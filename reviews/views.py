from django.shortcuts import render

from .models import Review

def get_all_reviews(request):
    latest_review_list = Review.objects.order_by('in_date')
    context = {
        'latest_review_list': latest_review_list,
    }
    return render(request, 'reviews/reviews.html', context)

# Create your views here.
