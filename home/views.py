from django.shortcuts import render

from registration import forms, utils
from reviews import utils as review_utils

def landing(request):
    if request.method == 'POST':
        result = utils.register_unapproved_stay(request.POST)
        print(result)
    template_name = 'home/home.html'
    reviews = review_utils.get_top_n_reviews(3)
    if len(reviews) != 0:
        result = render(request, template_name, {'reviews': review_utils.get_top_n_reviews(3)})
    else:
        result = render(request, template_name, {})
    return result
