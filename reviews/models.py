from django.db import models
from django.core import validators
from django.core.exceptions import ValidationError

from registration.models import Stay

import random

class Review(models.Model):
    corresponding_stay = models.OneToOneField(Stay, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=5, validators=[validators.MinValueValidator(1), validators.MaxValueValidator(5)])
    review_text = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    publish_date = models.DateField(blank=True, null=True)
    link_key = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f'{self.corresponding_stay.name}: {"Reviewed" if self.is_published else "Not Reviewed"}'

    def clean(self):
        super().clean()
        self.link_key = str(random.getrandbits(64))

