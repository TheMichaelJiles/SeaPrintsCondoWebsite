from django.urls import path

from registration import views as registration_views

urlpatterns = [
    path('get_taken_dates/', registration_views.get_taken_dates, name='taken-dates'),
    path('approve/<int:staypk>/', registration_views.approve_stay, name='approve-stay'),
    path('get_rates/', registration_views.get_rates, name='rates'),
    path('get_tax_info/', registration_views.get_tax_info, name='tax_info'),
    path('register/', registration_views.register, name='register'),
]