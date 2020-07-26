from django.http import JsonResponse, FileResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from django.utils.html import format_html

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
    result = utils.approve_stay(staypk)
    resulting_stay = result['stay']
    email_sender = utils.EmailSender()
    email_sender.send_guest(
        subject='SeaPrints: APPROVED',
        message=(
            'Your stay has been approved.\n\n'
            'Stay Details:\n'
            f'Name: {resulting_stay.guest.name}\n'
            f'Number of guests: {resulting_stay.number_of_guests}\n'
            f'Check-in Date: {resulting_stay.in_date}\n'
            f'Check-out Date: {resulting_stay.out_date}\n'
            f'Price: {"${:,.2f}".format(resulting_stay.total_price)}\n'
        ),
        guests=[resulting_stay.guest.email_contact,]
    )
    return redirect(reverse('admin:registration_stay_changelist'))

def register(request):
    if request.method == 'POST':
        register_result = utils.register_unapproved_stay(request.POST)
        if register_result['success']:
            messages.success(request, 'Thanks! You should hear from us within 24 hours!')
            new_stay = register_result['stay']
            email_sender = utils.EmailSender()
            link = f'http://localhost:8000{reverse("admin:registration_stay_change", args=(new_stay.pk,))}'
            email_sender.send_admin(
                subject='New Stay Requested',
                html_message=format_html(
                    '{} <a href="{}" target="_blank">{}</a>',
                    f'{new_stay.guest.name} has requested a stay. This still requires an approval.',
                    link,
                    'Click here to see the new stay request.',
                )
            )
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
