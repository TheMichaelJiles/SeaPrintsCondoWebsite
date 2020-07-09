from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from registration import api as data
from registration import utils
from registration import forms as registration_forms

def get_taken_dates(request):
    return JsonResponse(data.get_taken_dates(), safe=False)

def get_rates(request):
    return JsonResponse(data.get_rates(), safe=False)

def approve_stay(request, staypk):
    utils.approve_stay(staypk)
    return redirect(reverse('admin:registration_stay_changelist'))

def register(request):
    if request.method == 'POST':
        register_result = utils.register_unapproved_stay(request.POST)
        #if register_result['success']:
        print(register_result)
        result = redirect(reverse('landing'))
        # else redirect back to the same page saying an error occurred.
    else:
        result = render(request, 'registration/registration.html', {
            'form': registration_forms.CombinedStayAddressForm(),
            'helper': registration_forms.CombinedFormHelper()
        })
    return result
