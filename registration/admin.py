from django.contrib import admin
from .models import Stay, Address, SeasonPricing, Globals

# Register your models here.
admin.site.register(Stay)
admin.site.register(Address)
admin.site.register(SeasonPricing)
admin.site.register(Globals)