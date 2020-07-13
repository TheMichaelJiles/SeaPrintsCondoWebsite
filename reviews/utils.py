from django.core.exceptions import ValidationError

from registration.models import Stay
from reviews.models import Review

import datetime

def create_unpublished_review(stay_pk):
    try:
        target_stay = Stay.objects.get(pk=stay_pk)
        unpub_review = Review(corresponding_stay=target_stay)
        unpub_review.full_clean()
        unpub_review.save()

        result = {'success': True}
    except ValidationError as e:
        result = {
            'success': False,
            'error_source': 'reviews.utils.create_unpublished_review: Validation Failed.',
            'error_details': e.message_dict,}
    return result

def publish_review(link_key, postdata):
    try:
        target_review = Review.objects.get(link_key=link_key)
        target_review.rating = int(postdata['rating'])
        target_review.review_text = postdata['review_text']
        target_review.publish_date = datetime.datetime.now()
        target_review.is_published = True
        target_review.save()

        result = {'success': True}
    except ValidationError as e:
        result = {
            'success': False,
            'error_source': 'reviews.utils.publish_review: Validation Failed.',
            'error_details': e.message_dict,}
    return result

def get_all_reviews():
    return Review.objects.filter(is_published=True).order_by('-publish_date')

def get_top_n_reviews(n):
    return get_all_reviews()[:n]