from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('<int:page>/', views.get_all_reviews, name='all_reviews'),
    path('publish/<str:publishkey>/', views.write_review, name="write_review"),
]