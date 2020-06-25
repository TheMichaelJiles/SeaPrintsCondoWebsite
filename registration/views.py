from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse

from registration import api as data
from registration import utils

def get_taken_dates(request):
    return JsonResponse(data.get_taken_dates(), safe=False)

def approve_stay(request, staypk):
    utils.approve_stay(staypk)
    return redirect(reverse('admin:registration_stay_changelist'))
