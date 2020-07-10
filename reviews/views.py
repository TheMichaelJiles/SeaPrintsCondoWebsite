from django.shortcuts import render, redirect

from reviews import forms, utils
from reviews.models import Review

REVIEWS_PER_PAGE = 5

def get_all_reviews(request, page):
    all_reviews = utils.get_all_reviews()
    max_pages = (all_reviews.count() // REVIEWS_PER_PAGE) + 1
    if page > max_pages:
        target_page = max_pages
    elif page < 1:
        target_page = 1
    else:
        target_page = page
    start_index = REVIEWS_PER_PAGE * (target_page - 1)
    end_index = min((start_index + REVIEWS_PER_PAGE), all_reviews.count())
    review_list = all_reviews[start_index:end_index]
    return render(request, 'reviews/reviews.html', {
        'review_list': review_list,
        'current_page': page,
        'is_first_page': page == 1,
        'is_last_page': page == max_pages,
        'next_page': page + 1,
        'previous_page': page - 1,
    })

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
