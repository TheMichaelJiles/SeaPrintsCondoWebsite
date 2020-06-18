from django.shortcuts import render

from reviews import forms
from .models import Review

def get_all_reviews(request):
    latest_review_list = Review.objects.order_by('in_date')
    context = {
        'latest_review_list': latest_review_list,
    }
    return render(request, 'reviews/reviews.html', context)

def write_review(request):
    return render(request, 'reviews/review_form.html', {'form': forms.ReviewForm()})
