import datetime
from rest_framework import serializers
from .models import *


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Userprofile
        fields = ['id', 'url', 'username', 'gender', 'date_of_birth']


class CouponSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'gender', 'start_date', 'end_date', 'discount',
                  'discount_type', 'max_coupon', 'user_limit', 'owner']

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError('please select future date in end date')
        return data

        # if data['discount'] > 100:
        #     if data['discount_type'] == 'Percentage':
        #         raise serializers.ValidationError('percentage can be enter up to 100')


class OrderSerializer(serializers.ModelSerializer):
    total_amount = serializers.SerializerMethodField('get_total')
    discount_amount = serializers.SerializerMethodField('get_discount')

    class Meta:
        model = Order
        fields = ['id', 'coupon', 'order_amount', 'total_amount', 'discount_amount', 'owner']

    def get_total(self, coupon):
        discount = coupon.coupon.discount
        discount_type = coupon.coupon.discount_type
        order_amount = coupon.order_amount

        user = Userprofile.objects.all().first()
        birth_date = datetime.datetime.strftime(user.date_of_birth, "%d-%m")
        today_date = datetime.date.today()
        valid_date = datetime.datetime.strftime(today_date, "%d-%m")

        if discount_type == 'Flat':
            if birth_date == valid_date:
                total = order_amount - discount
                total_amounts = total - (total * 0.1)
            else:
                total_amounts = order_amount - discount
        else:
            if birth_date == valid_date:
                dis = order_amount * (discount / 100)
                total = order_amount - dis
                total_amounts = total - (total * 0.1)
            else:
                dis = order_amount * (discount / 100)
                total_amounts = order_amount - dis

        coupon.total_amount = total_amounts
        coupon.save()
        return coupon.total_amount

    def get_discount(self, coupon):
        discount = coupon.coupon.discount
        discount_type = coupon.coupon.discount_type
        order_amount = coupon.order_amount

        user = Userprofile.objects.all().first()
        birth_date = datetime.datetime.strftime(user.date_of_birth, "%d-%m")
        today_date = datetime.date.today()
        valid_date = datetime.datetime.strftime(today_date, "%d-%m")

        if discount_type == "FLAT":
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
