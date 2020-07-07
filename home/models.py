from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

class Globals(models.Model):
    '''
    The globals model should only ever have one row. This row contains
    site wide data related to registration that the registration services
    rely on.
    '''
    default_price_per_night = models.FloatField(default=175, validators=[MinValueValidator(0),])
    minimum_days_of_stay = models.IntegerField(default=4, validators=[MinValueValidator(0),])
    cleaning_fee = models.FloatField(default=150, validators=[MinValueValidator(0),])
    tax_rate_percent = models.IntegerField(default=12, validators=[MinValueValidator(0), MaxValueValidator(100),])

    def __str__(self):
        return 'Site Setting'

    def clean(self):
        '''
        This is an overriden version of the clean method from models.Model.
        The partial override ensures that no more than one row is created in
        the table. A Globals object should never be instantiated manually. Instead,
        it should be created through a ModelForm on the admin page.
        '''
        super().clean()
        if Globals.objects.all().count() > 0:
            raise ValidationError(('There is already a global setting entry. Modify it instead of creating a new setting.'))
