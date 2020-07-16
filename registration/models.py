import datetime

from django.db import models
from django.core.exceptions import ValidationError
from django.core import validators

from home.models import Globals
from phonenumber_field.modelfields import PhoneNumberField
from registration import api as data

class SeasonPricing(models.Model):
    '''
    This model is used to calculate the price of stays. The entries are added only
    through the admin page; therefore, a SeasonPricing object should never be created manually.
    Instead, it should be created through the use of a ModelForm.
    '''
    start_date = models.DateField('season start date', unique=True)
    end_date = models.DateField('season end date', unique=True)
    price_per_night = models.FloatField()

    def __str__(self):
        return f'{str(self.start_date)} to {str(self.end_date)} : ${self.price_per_night}/night'

    def clean(self):
        '''
        This is an overriden version of the models.Model clean() method. The partial override performs
        additional validation. It ensures that the price per night is positive. It ensures that the start
        date for the season comes before the ending date for the season. It also ensures that the new season
        does not conflict with an already existing season.
        '''
        super().clean()
        self._perform_additional_validation()

    def _perform_additional_validation(self):
        self._ensure_price_is_positive()
        self._ensure_season_start_is_before_season_end()
        self._ensure_does_not_conflict_with_existing_season()

    def _ensure_price_is_positive(self):
        if self.price_per_night < 0:
            raise ValidationError(('The price per night should not be less than 0.'))

    def _ensure_season_start_is_before_season_end(self):
        if self.start_date > self.end_date:
            raise ValidationError(('Season start date must be before or the same as the season end date.'))

    def _ensure_does_not_conflict_with_existing_season(self):
        current_seasons = SeasonPricing.objects.all()
        for season in current_seasons:
            if self.end_date > season.start_date and self.start_date < season.start_date:
                raise ValidationError(('Season conflicts with an already existing season.'))
            if self.start_date < season.start_date and self.end_date > season.end_date:
                raise ValidationError(('Season conflicts with an already existing season.'))

class Address(models.Model):
    '''
    This model is used to store the addresses for customers that register stays.
    Take the example address: 16 Chicken Street Carrollton, GA 30118 United States
    The fields would correspond as follows:
    street_number = '16'
    route = 'Chicken Street'
    city = 'Carrollton'
    state = 'GA'
    zip_code = '30118'
    country = 'United States'
    '''
    street_number = models.CharField(max_length=10)
    route = models.CharField(max_length=25)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=25)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=25)

    def __str__(self):
        return f'{self.street_number} {self.route}\n{self.city}, {self.state} {self.zip_code}\n{self.country}'

class Guest(models.Model):
    name = models.CharField(max_length=20)
    age = models.PositiveIntegerField(default=25, validators=[validators.MinValueValidator(25),])
    phone_contact = PhoneNumberField(null=False, blank=False, unique=False)
    email_contact = models.EmailField()
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    is_discount_eligible = models.BooleanField(default=False)

class GuestNotes(models.Model):
    guest = models.OneToOneField(Guest, on_delete=models.CASCADE)
    notes = models.TextField(default='', blank=True)

class Stay(models.Model):
    '''
    This is the model field that stores information about a stay.
    By default, new stays are not approved. The only optional field is the
    additional questions or concerns field. Each stay entry is linked to one
    Address entry. When creating a Stay object manually, call the full_clean()
    method before the save() method is called and catch any ValidationErrors to 
    ensure the Stay is created with valid data.
    '''
    class Meta:
        ordering = ['is_approved', 'in_date', 'guest']

    guest = models.OneToOneField(Guest, on_delete=models.PROTECT)
    in_date = models.DateField('check-in date', unique=True)
    out_date = models.DateField('check-out date', unique=True)
    total_price = models.FloatField(default=0, validators=[validators.MinValueValidator(0),])
    number_of_guests = models.PositiveIntegerField(default=1, validators=[validators.MinValueValidator(1), validators.MaxValueValidator(6)])
    is_approved = models.BooleanField(default=False)
    is_fully_paid = models.BooleanField(default=False)
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    additional_questions_or_concerns = models.TextField(default='', blank=True)

    def __str__(self):
        return f'{self.guest.name}: {"APPROVED" if self.is_approved else "PENDING"}'

    def clean(self):
        '''
        This is the partial overriden version of the models.Model's clean method.
        It performs additional validation to ensure data is sufficient. Then, once the
        data is validated, calculates the total cost of the stay depending on the seasons.
        '''
        super().clean()
        self._perform_additional_validation()
        self._set_calculated_total_price()
    
    def _perform_additional_validation(self):
        self._ensure_checkout_occurs_before_checkin()
        self._ensure_global_setting_is_set()
        self._ensure_at_least_minimum_days_of_stay()
        self._ensure_no_conflicts_with_existing_stays()
        self._ensure_valid_number_of_guests()

    def _ensure_checkout_occurs_before_checkin(self):
        if self.in_date >= self.out_date:
            raise ValidationError(('The check-in date must be before the check-out date.'))

    def _ensure_global_setting_is_set(self):
        if Globals.objects.all().count() != 1:
            raise ValidationError(('Administrative Error: Globals not set.'))

    def _ensure_at_least_minimum_days_of_stay(self):
        num_days = (self.out_date - self.in_date).days
        global_setting = Globals.objects.get(pk=1)
        if num_days < global_setting.minimum_days_of_stay:
            raise ValidationError((f'A minimum of {global_setting.minimum_days_of_stay} day(s) required.'))

    def _ensure_no_conflicts_with_existing_stays(self):
        num_days = (self.out_date - self.in_date).days
        taken_dates = data.get_taken_dates()
        for x in range(0, num_days):
            current_date = self.in_date + datetime.timedelta(days=x)
            if current_date in taken_dates:
                raise ValidationError(('One or more dates of stay conflict with a current approved visit.'))

    def _ensure_valid_number_of_guests(self):
        if self.number_of_guests < 1:
            raise ValidationError(('There must be at least one guest.'))

    def _set_calculated_total_price(self):
        num_days = (self.out_date - self.in_date).days
        self.total_price = 0
        for x in range(0, num_days):
            current_date = self.in_date + datetime.timedelta(days=x)
            price_for_day = self._get_rate(current_date)
            self.total_price += price_for_day
        global_obj = Globals.objects.get(pk=1)
        self.total_price += global_obj.cleaning_fee
        self.total_price *= ((global_obj.tax_rate_percent / 100.0) + 1)

    def _get_rate(self, date):
        price = Globals.objects.get(pk=1).default_price_per_night
        seasons = SeasonPricing.objects.all()
        for season in seasons:
            if date > season.start_date and date < season.end_date:
                price = season.price_per_night
        return price