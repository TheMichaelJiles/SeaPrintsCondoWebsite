from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from reviews.models import Review

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['modify_review', 'get_stay_name', 'is_published', 'get_rating', 'get_publish_date']

    def modify_review(self, obj):
        return 'View'
    modify_review.short_description = 'Customer Reviews'

    def get_stay_name(self, obj):
        anchor = f'<a href="{reverse("admin:registration_stay_change", args=(obj.corresponding_stay.pk,))}">{obj.corresponding_stay.name}</a>'
        return format_html(anchor)
    get_stay_name.short_description = 'Customer Name'

    def get_rating(self, obj):
        if obj.is_published:
            result = obj.rating
        else:
            result = ''
        return result
    get_rating.short_description = 'Rating'

    def get_publish_date(self, obj):
        if obj.is_published:
            result = obj.publish_date
        else:
            result = ''
        return result
    get_publish_date.short_description = 'Publish Date'

admin.site.register(Review, ReviewAdmin)
