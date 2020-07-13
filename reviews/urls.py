from django.contrib import admin
from django.urls import path, include

from reviews import views as reviews_views

urlpatterns = [
    path('<int:page>/', reviews_views.get_all_reviews, name='all_reviews'),
    path('publish/<str:publishkey>/', reviews_views.write_review, name="write_review"),
]