from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Stay(models.Model):
    name = models.CharField(max_length=20)
    in_date = models.DateTimeField('check-in date')
    out_date = models.DateTimeField('check-out date')
    total_price = models.FloatField()
    phone_contact = PhoneNumberField(null=False, blank=False, unique=True)
    email_contact = models.EmailField()
    number_of_guests = models.IntegerField(default=1)