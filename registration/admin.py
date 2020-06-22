from django.contrib import admin
from django import forms

from registration.models import Stay, Address, SeasonPricing, Globals

class StayAdmin(admin.ModelAdmin):
    exclude = ('is_approved',)

admin.site.register(Stay, StayAdmin)
admin.site.register(Address)
admin.site.register(SeasonPricing)
admin.site.register(Globals)