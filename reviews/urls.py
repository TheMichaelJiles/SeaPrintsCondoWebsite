from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.get_all_reviews, name='all_reviews'),
    path('write_review/', views.write_review, name="write_review"),
]