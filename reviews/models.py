from django.db import models
from django.core import validators

from registration.models import Stay

import datetime, random

class Review(models.Model):
    corresponding_stay = models.ForeignKey(Stay, on_delete=models.PROTECT)
    rating = models.PositiveIntegerField(default=5, blank=True, null=True, validators=[validators.MinValueValidator(1), validators.MaxValueValidator(5)])
    review_text = models.TextField(required=False, blank=True, null=True)
    is_published = models.BooleanField(default=False)
    publish_date = models.DateField(required=False, blank=True, null=True)
    link_key = models.CharField(max_length=19)

    def __str__(self):
        return f'{self.corresponding_stay.name}: {"Reviewed" if self.is_published else "Not Reviewed"}'

    def clean(self):
        super().clean()
        self.link_key = str(random.getrandbits(64))
