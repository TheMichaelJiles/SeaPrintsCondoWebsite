from django.contrib import admin, messages
from django.contrib.admin.views.main import ChangeList
from django import forms
from django.utils.translation import ngettext
from django.utils.html import format_html
from django.urls import reverse
from datetime import datetime
from django.db.models import Q

from registration.models import Stay, Address, SeasonPricing, Guest
from registration import utils as registration_utils

class DateFilter(admin.SimpleListFilter):
    title = 'Date Stayed'

    parameter_name = 'date'

    def lookups(self, request, stay_admin):
        return(
            ('past', ('past stays')),
            ('present', ('current stays')),
            ('future', ('future stays')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'present':
            return queryset.filter(Q(out_date=datetime.date(datetime.now())) | Q(in_date=datetime.date(datetime.now())))
        elif self.value() == 'past':
            return queryset.filter(out_date__lte=datetime.date(datetime.now()))
        elif self.value() == 'future':
            return queryset.filter(in_date__gte=datetime.date(datetime.now()))

class NameFilter(admin.SimpleListFilter):
    title = 'Name'
    template = 'admin/name_filter.html'

    parameter_name = 'name'

    def lookups(self, request, stay_admin):
        return ((),)

    def queryset(self, request, queryset):
        term = self.value()

        if term == "" or term is None:
            return queryset

        result = queryset.filter(guest__name__icontains=term)

        return result

    def choices(self, changelist):
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice

class StayAdmin(admin.ModelAdmin):
    list_display = ['modify_stay', 'show_guest_link', 'is_approved', 'in_date', 'out_date', 'show_total_price', 'is_using_custom_price', 'is_fully_paid']
    list_filter = (DateFilter, NameFilter, )
    exclude = ('is_approved',)
    actions = ['approve_selected_stays', 'show_past_stays']

    def modify_stay(self, obj):
        return 'View'
    modify_stay.short_description = 'Modify'

    def show_guest_link(self, obj):
        return format_html(f'<a href="{reverse("admin:registration_guest_change", args=(obj.guest.pk,))}">{obj.guest.name}</a>')
    show_guest_link.short_description = 'Guest'

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

class AddressAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'show_linked_stay_name']

    def show_linked_stay_name(self, obj):
        try:
            linked_stays = Stay.objects.filter(address=obj)
            stay_anchor_string = map(
                lambda stay: f'<a href="{reverse("admin:registration_stay_change", args=(stay.pk,))}">{stay.name}</a>', 
                linked_stays)
            result = format_html(', '.join(stay_anchor_string))
        except:
            result = 'No Linked Stay'
        return result
    show_linked_stay_name.short_description = 'Customer(s)'
    show_linked_stay_name.allow_tags = True

class SeasonPricingAdmin(admin.ModelAdmin):
    list_display = ['modify_season', 'start_date', 'end_date', 'show_price_per_night']

    def show_price_per_night(self, obj):
        return '${:,.2f}'.format(obj.price_per_night)
    show_price_per_night.short_description = 'Price / Night'

    def modify_season(self, obj):
        return 'View'
    modify_season.short_description = 'Seasonal Pricing'

admin.site.register(Stay, StayAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(SeasonPricing, SeasonPricingAdmin)
admin.site.register(Guest)