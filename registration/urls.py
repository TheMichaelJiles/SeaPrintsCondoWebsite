from django.urls import path

from . import views

urlpatterns = [
    path('get_taken_dates/', views.get_taken_dates, name='taken-dates'),
]