import datetime
from django.db import models
from django.core.exceptions import ValidationError

from phonenumber_field.modelfields import PhoneNumberField
from registration import registration as data

# Create your models here.

class Globals(models.Model):
    default_price_per_night = models.FloatField(default=175)
    minimum_days_of_stay = models.IntegerField(default=4)

    def __str__(self):
        return 'Site Setting'

    def clean(self):
        super().clean()
        if Globals.objects.all().count() > 0:
            raise ValidationError(('There is already a global setting entry. Modify it instead of creating a new setting.'))

class SeasonPricing(models.Model):
    start_date = models.DateField('season start date', unique=True)
    end_date = models.DateField('season end date', unique=True)
    price_per_night = models.FloatField()

    def __str__(self):
        return f'{str(self.start_date)} to {str(self.end_date)} : ${self.price_per_night}/night'

    def clean(self):
        super().clean()
        if self.start_date > self.end_date:
            raise ValidationError(('Season start date must be before or the same as the season end date.'))
        current_seasons = SeasonPricing.objects.all()
        for season in current_seasons:
            if self.end_date > season.start_date and self.start_date < season.start_date:
                raise ValidationError(('Season conflicts with an already existing season.'))
            if self.start_date < season.start_date and self.end_date > season.end_date:
                raise ValidationError(('Season conflicts with an already existing season.'))

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
    in_date = models.DateField('check-in date', unique=True)
    out_date = models.DateField('check-out date', unique=True)
    total_price = models.FloatField(default=0)
    phone_contact = PhoneNumberField(null=False, blank=False, unique=False)
    email_contact = models.EmailField()
    number_of_guests = models.IntegerField(default=1)
    is_approved = models.BooleanField(default=False)
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    additional_questions_or_concerns = models.TextField(default='', blank=True)

    def __str__(self):
        return f'{self.name}: {"APPROVED" if self.is_approved else "PENDING"}'

    def clean(self):
        super().clean()
        start = self.in_date
        end = self.out_date

        if start >= end:
            raise ValidationError(('The check-in date must be before the check-out date.'))

        num_days = (end - start).days
        if Globals.objects.all().count() != 1:
            raise ValidationError(('Administrative Error: Globals not set.'))
        global_setting = Globals.objects.get(pk=1)
        if num_days < global_setting.minimum_days_of_stay:
            raise ValidationError((f'A minimum of {global_setting.minimum_days_of_stay} day(s) required.'))

        taken_dates = data.get_taken_dates()
        for x in range(0, num_days):
            current_date = start + datetime.timedelta(days=x)
            if current_date in taken_dates:
                raise ValidationError(('One or more dates of stay conflict with a current approved visit.'))
        
        if self.number_of_guests < 1:
            raise ValidationError(('There must be at least one guest.'))
        
        self.total_price = 0
        for x in range(0, num_days):
            current_date = start + datetime.timedelta(days=x)
            price_for_day = self.get_rate(current_date)
            self.total_price += price_for_day
    
    def get_rate(self, date):
        price = Globals.objects.get(pk=1).default_price_per_night
        seasons = SeasonPricing.objects.all()
        for season in seasons:
            if date > season.start_date and date < season.end_date:
                price = season.price_per_night
        return price