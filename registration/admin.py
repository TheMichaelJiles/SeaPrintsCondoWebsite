from django.contrib import admin, messages
from django.contrib.admin.views.main import ChangeList
from django import forms
from django.utils.translation import ngettext

from registration.models import Stay, Address, SeasonPricing, Globals
from registration import utils as registration_utils

class StayAdmin(admin.ModelAdmin):
    list_display = ['name', 'in_date', 'out_date', 'is_approved', 'show_total_price']
    exclude = ('is_approved',)
    actions = ['approve_selected_stays']

    def show_total_price(self, obj):
        return '${:,.2f}'.format(obj.total_price)
    show_total_price.short_description = 'Total Price'

    def approve_selected_stays(self, request, queryset):
        unapproved_stays = queryset.filter(is_approved=False)
        approval_count = 0
        for stay in unapproved_stays:
            result = registration_utils.approve_stay(stay.pk)
            if result['success']:
                approval_count += 1
        if approval_count > 0:
            self.message_user(request, ngettext(
                '%d stay was successfully approved.',
                '%d stays were successfully approved.',
                approval_count,
            ) % approval_count, messages.SUCCESS)
        if approval_count < queryset.count():
            delta = queryset.count() - approval_count
            self.message_user(request, ngettext(
                '%d stay was already approved.',
                '%d stays were already approved.',
                delta,
            ) % delta, messages.ERROR)
    approve_selected_stays.short_description = 'Approve selected stays'

admin.site.register(Stay, StayAdmin)
admin.site.register(Address)
admin.site.register(SeasonPricing)
admin.site.register(Globals)