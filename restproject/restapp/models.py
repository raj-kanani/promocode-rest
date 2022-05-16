from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from datetime import date
from django.core.exceptions import ValidationError


class Userprofile(AbstractUser):
    gender_choice = (("MALE", "Male"), ("FEMALE", "Female"),)

    gender = models.CharField(choices=gender_choice, default="MALE", max_length=6)
    date_of_birth = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.username)


class Coupon(models.Model):
    code = models.CharField(max_length=10, unique=True,
                            validators=[RegexValidator(
                                "^[A-Z0-9]*$", "code enter must be uppercase letters & numbers",
                            )], null=True, blank=True)
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),)
    gender = models.CharField(max_length=7, choices=GENDER_CHOICES)

    def validate_date(end_date):
        today = date.today()
        if end_date < today:
            raise ValidationError("You can not enter past dates because coupon is expired.")

    start_date = models.DateField()
    end_date = models.DateField(validators=[validate_date])
    # help_text : field in suggestion message provide
    discount = models.IntegerField(help_text='enter discount under 100', default=None, validators=[MaxValueValidator(100)])

    TYPE_CHOICES = [('Flat', 'Flat'),
                    ('Percentage', 'Percentage')]

    discount_type = models.CharField(choices=TYPE_CHOICES, default='Flat', max_length=10)
    max_coupon = models.IntegerField(null=True, default=1)
    user_limit = models.IntegerField(null=True)
    owner = models.ForeignKey(Userprofile, related_name='user', on_delete=models.CASCADE, null=True)

    def clean(self):
        super().clean()
        if not (self.start_date <= self.end_date):
            raise ValidationError("Don't select Invalid start and end date")

    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        return super(Coupon, self).save(*args, **kwargs)

    def __str__(self):
        return self.code


class Order(models.Model):
    code = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='coupon_related')
    order_amount = models.IntegerField(validators=[MinValueValidator(100), MaxValueValidator(1500000)])
    total_amount = models.IntegerField(null=True)
    user = models.ForeignKey(Userprofile, on_delete=models.CASCADE, related_name='user_related', null=True)
