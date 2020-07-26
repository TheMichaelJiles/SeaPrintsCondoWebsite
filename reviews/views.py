from django.shortcuts import render, redirect

from reviews import forms as reviews_forms
from reviews import utils
from reviews.models import Review

REVIEWS_PER_PAGE = 5

def get_all_reviews(request, page):
    all_reviews = utils.get_all_reviews()
    if all_reviews.count() > 5:
        max_pages = (all_reviews.count() // REVIEWS_PER_PAGE) + 1
    else:
        max_pages = 1
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
        'current_page': target_page,
        'is_first_page': target_page == 1,
        'is_last_page': target_page == max_pages,
        'next_page': target_page + 1,
        'previous_page': target_page - 1,
        'is_reviews_empty': all_reviews.count() == 0,
    })

def write_review(request, publishkey):
    if request.method == 'POST':
        # This is when they submit the review form.
        post_result = utils.publish_review(publishkey, request.POST)
        print('Review Posted')
        result = redirect('landing')
    elif not Review.objects.filter(link_key=publishkey).exists():
        # This means that the publish key is incorrect or does not exist.
        print('Review Publish Key Does Not Exist.')
        result = redirect('landing')
    else:
        # This loads the initial review form page if the publish key is successful.
        review_data = Review.objects.get(link_key=publishkey)
        if review_data.is_published:
            # Redirect while alerting user they have already submitted their review.
            print('Review with specified published key already posted.')
            result = redirect('landing')
        else:
            result = render(request, 'reviews/review_form.html', {
                'form': reviews_forms.ReviewForm(), 
                'helper': reviews_forms.ReviewFormHelper(), 
                'data': review_data
            })
    return result
