from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_exempt

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

@xframe_options_exempt
def register(request):
    return render(request, 'registration/registration.html', {
        'form': registration_forms.CombinedStayAddressForm(),
        'helper': registration_forms.CombinedFormHelper()
    })
