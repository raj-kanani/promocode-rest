# Generated by Django 4.0.4 on 2022-05-12 05:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restapp', '0002_remove_coupon_owner_remove_coupon_promo_code_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coupon',
            old_name='discounttype',
            new_name='discount_type',
        ),
        migrations.RenameField(
            model_name='coupon',
            old_name='max_coupen',
            new_name='max_coupon',
        ),
    ]