from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from registration import forms

def landing(request):
    if request.method == 'POST':
        print(request.POST)
    template_name = 'home/home.html'
    return render(request, template_name, {'form': forms.StayForm()})