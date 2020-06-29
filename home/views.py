from django.shortcuts import render

from registration import forms, utils
from reviews import utils as review_utils

def landing(request):
    if request.method == 'POST':
        result = utils.register_unapproved_stay(request.POST)
        print(result)
    template_name = 'home/home.html'
    # return render(request, template_name, {'form': forms.StayForm(), 'address_form': forms.AddressForm()})
    return render(request, template_name, {'reviews': review_utils.get_top_n_reviews(3)})
