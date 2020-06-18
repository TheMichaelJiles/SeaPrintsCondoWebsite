from django.shortcuts import render

from registration import forms
from registration import validation

def landing(request):
    if request.method == 'POST':
        print(request.POST)
        was_successful = validation.process_post_data(request.POST)
    template_name = 'home/home.html'
    return render(request, template_name, {'form': forms.StayForm(), 'address_form': forms.AddressForm()})