from django.shortcuts import render

from registration import forms, utils

def landing(request):
    if request.method == 'POST':
        result = utils.register_unapproved_stay(request.POST)
        print(result)
    template_name = 'home/home.html'
    return render(request, template_name, {'form': forms.StayForm(), 'address_form': forms.AddressForm()})