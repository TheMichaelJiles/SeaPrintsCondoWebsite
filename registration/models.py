from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Address(models.Model):
    street_number = models.CharField(max_length=10)
    route = models.CharField(max_length=25)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=25)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=25)

    def __str__(self):
        return f'{self.street_number} {self.route}\n{self.city}, {self.state} {self.zip_code}\n{self.country}'

class Stay(models.Model):
    name = models.CharField(max_length=20)
    in_date = models.DateTimeField('check-in date')
    out_date = models.DateTimeField('check-out date')
    total_price = models.FloatField()
    phone_contact = PhoneNumberField(null=False, blank=False, unique=True)
    email_contact = models.EmailField()
    number_of_guests = models.IntegerField(default=1)
    is_approved = models.BooleanField(default=False)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}: {"APPROVED" if self.is_approved else "PENDING"}'