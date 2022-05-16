import datetime
from django.utils import timezone
from rest_framework import serializers
from .models import *


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Userprofile
        fields = ['id', 'url', 'username', 'gender', 'date_of_birth']


class CouponSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'url', 'code', 'gender', 'start_date', 'end_date', 'discount',
                  'discount_type', 'max_coupon', 'user_limit', 'owner']


class OrderSerializer(serializers.ModelSerializer):
    # total_amount = serializers.SerializerMethodField('get_total')
    discount_amount = serializers.SerializerMethodField('get_discount')

    class Meta:
        model = Order
        fields = ['id', 'code', 'order_amount', 'total_amount', 'discount_amount', 'user']

    # def get_total(self, code):
    #     discount = code.code.discount
    #     discount_type = code.code.discount_type
    #     order_amount = code.order_amount
    #
    #     user = Userprofile.objects.all().first()
    #     birth_date = datetime.datetime.strftime(user.date_of_birth, "%d-%m")
    #     today_date = datetime.date.today()
    #     valid_date = datetime.datetime.strftime(today_date, "%d-%m")
    #
    #     if discount_type == 'Flat':
    #         if birth_date == valid_date:
    #             total = order_amount - discount
    #             total_amounts = total - (total * 0.1)
    #         else:
    #             total_amounts = order_amount - discount
    #     else:
    #         if birth_date == valid_date:
    #             dis = order_amount * (discount / 100)
    #             total = order_amount - dis
    #             total_amounts = total - (total * 0.1)
    #         else:
    #             dis = order_amount * (discount / 100)
    #             total_amounts = order_amount - dis
    #
    #     code.total_amount = total_amounts
    #     code.save()
    #     return code.total_amount

    def get_discount(self, code):
        discount = code.code.discount
        discount_type = code.code.discount_type
        order_amount = code.order_amount

        user = Userprofile.objects.all().first()
        birth_date = datetime.datetime.strftime(user.date_of_birth, "%d-%m")
        today_date = datetime.date.today()
        valid_date = datetime.datetime.strftime(today_date, "%d-%m")

        if discount_type == "Flat":
            if birth_date == valid_date:
                total = order_amount - discount
                discount_amount = discount + (total * 0.1)
            else:
                discount_amount = discount
        else:
            if birth_date == valid_date:
                dis = order_amount * (discount / 100)
                total = order_amount - dis
                discount_amount = dis + (total * 0.1)
            else:
                dis = order_amount * (discount / 100)
                discount_amount = dis
        return discount_amount

    def validate(self, attrs):
        code = attrs.pop('code', None)
        order_amount = attrs.get('order_amount', None)
        if not Coupon.objects.filter(code=code).exists():
            raise serializers.ValidationError("Coupon code not found!")

        code = Coupon.objects.get(code=code)
        user = self.context.get('request').user
        user_birth = Userprofile.objects.filter(date_of_birth=user.date_of_birth).first()

        if code.discount_type == "Flat":
            total_amount = order_amount - code.discount
        else:
            date_of_birth = user_birth.date_of_birth
            valid_date = timezone.now().date().strftime("%m-%d")

            if date_of_birth and date_of_birth.strftime("%m-%d") == valid_date:
                discount = order_amount * (code.discount / 100)
                total = order_amount - discount
                total_amount = total - (total * 0.1)

            else:
                discount = order_amount * (code.discount / 100)
                total_amount = order_amount - discount

        max_coupon = code.max_coupon
        user_limit = code.user_limit

        if user.is_authenticated:
            user_count = len(Order.objects.filter(user=user, code=code))
            coupon_count = len(Order.objects.filter(code=code))

            if coupon_count > user_limit:
                raise serializers.ValidationError("Coupon limit is over")

            if user_count > max_coupon:
                raise serializers.ValidationError("Per user limit is over")

            code.max_coupon = code.max_coupon - 1
            code.save()
            # code.user_limit = code.user_limit - 1
            # code.save()
        else:
            raise serializers.ValidationError("choose different coupon or coupon limit is over")

        attrs['code'] = code
        attrs['user_id'] = user.id
        attrs['total_amount'] = total_amount
        return attrs

