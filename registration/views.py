from django.http import JsonResponse
from registration import registration as data

def get_taken_dates(request):
    return JsonResponse(data.get_taken_dates(), safe=False)