from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from registration import forms
from registration import validation

def landing(request):
    if request.method == 'POST':
        print(request.POST)
        was_successful = validation.process_post_data(request.POST)
        if was_successful:
            # Redirect to success page.
        else:
            # Redirect back to registration page with error shown.
    template_name = 'home/home.html'
    return render(request, template_name, {'form': forms.StayForm()})