from django.contrib import admin
from .models import *


@admin.register(Userprofile)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'gender', 'date_of_birth']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'gender', 'start_date', 'end_date', 'discount',
                    'discount_type', 'max_coupon', 'user_limit', 'owner']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['coupon', 'order_amount', 'total_amount', 'owner']
