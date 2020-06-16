from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def landing(request):
    template_name = 'home/home.html'
    return render(request, template_name)
# Create your views here.
