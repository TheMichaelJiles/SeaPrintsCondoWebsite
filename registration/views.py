from django.http import JsonResponse, FileResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from registration import api as data
from registration import utils
from registration import forms as registration_forms

def get_taken_dates(request):
    return JsonResponse(data.get_taken_dates(), safe=False)

def get_rates(request):
    return JsonResponse(data.get_rates(), safe=False)

def get_tax_info(request):
    if request.method == 'POST':
        filtered_stays = utils.get_filtered_stays_for_tax(request.POST)
        tax_info = utils.TaxInfo(stays=filtered_stays)
        pdf_buffer = utils.get_tax_pdf_buffer(tax_info)
        result = FileResponse(pdf_buffer, as_attachment=True, filename='tax-information.pdf')
    else:
        result = redirect(reverse('landing'))
    return result

def approve_stay(request, staypk):
    utils.approve_stay(staypk)
    return redirect(reverse('admin:registration_stay_changelist'))

def register(request):
    if request.method == 'POST':
        register_result = utils.register_unapproved_stay(request.POST)
        if register_result['success']:
            messages.success(request, 'Successfully Processed Stay Request.')
            result = redirect(reverse('landing'))
        else:
            error_descriptions = []
            for source, descriptions in register_result['error_details'].items():
                for description in descriptions:
                    error_descriptions.append(description)
            result = render(request, 'registration/registration.html', {
                'form': registration_forms.CombinedStayAddressForm(),
                'helper': registration_forms.CombinedFormHelper(),
                'errors': error_descriptions,
            })
    else:
        result = render(request, 'registration/registration.html', {
            'form': registration_forms.CombinedStayAddressForm(),
            'helper': registration_forms.CombinedFormHelper()
        })
    return result
