from django.shortcuts import render

from registration import forms
from registration import validation

def landing(request):
    if request.method == 'POST':
        result = validation.process_post_data(request.POST)
        print(result)
    template_name = 'home/home.html'
    return render(request, template_name, {'form': forms.StayForm(), 'address_form': forms.AddressForm()})