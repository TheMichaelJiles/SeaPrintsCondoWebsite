from django.shortcuts import render, redirect

from reviews import forms, utils
from reviews.models import Review

def get_all_reviews(request):
    latest_review_list = Review.objects.filter(is_published=True).order_by('publish_date')
    return render(request, 'reviews/reviews.html', {'latest_review_list': latest_review_list})

def write_review(request, publishkey):
    if request.method == 'POST':
        post_result = utils.publish_review(publishkey, request.POST)
        print(post_result)

        result = redirect('landing')
    elif not Review.objects.filter(link_key=publishkey).exists():
        result = redirect('landing')
    else:
        review_data = Review.objects.get(link_key=publishkey)
        result = render(request, 'reviews/review_form.html', {'form': forms.ReviewForm(), 'data': review_data})
    return result
