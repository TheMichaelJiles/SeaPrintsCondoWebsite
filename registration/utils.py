from django.core.exceptions import ValidationError

from dateutil import parser

from reportlab.platypus import SimpleDocTemplate, Table, Paragraph
from reportlab.lib.styles import ParagraphStyle
import io

from registration.models import Stay, Address
from home.models import Globals
from reviews import utils as reviews_utils

class TaxInfo:
    def __init__(self, stays=Stay.objects.all()):
        self.stays = stays
        self.global_obj = Globals.objects.get(pk=1)

    def get_stays(self):
        return self.stays

    def get_nights_rented(self):
        total_nights = 0
        for curr_stay in self.stays:
            if curr_stay.total_price > 0:
                date_delta = curr_stay.out_date - curr_stay.in_date
                total_nights += date_delta.days
        return total_nights

    def get_total_income(self):
        total_income = 0
        for curr_stay in self.stays:
            curr_total_price = curr_stay.total_price / ((self.global_obj.state_tax_rate_percent + self.global_obj.county_tax_rate_percent + 100) / 100)
            total_income += curr_total_price
        return total_income

    def get_unadjusted_county_tax(self):
        return self.get_total_income() * (self.global_obj.county_tax_rate_percent / 100)

    def get_adjusted_county_tax(self):
        return self.get_unadjusted_county_tax() * 0.975

    def get_unadjusted_state_tax(self):
        return self.get_total_income() * (self.global_obj.state_tax_rate_percent / 100)

    def get_adjusted_state_tax(self):
        return self.get_unadjusted_state_tax() * 0.975

def get_tax_pdf_buffer(tax_info):
    pdf_buffer = io.BytesIO()
    pdf = SimpleDocTemplate(pdf_buffer, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    title_para_style = ParagraphStyle(
        name='title',
        fontSize=24,
        spaceAfter=30,
    )
    header_para_style = ParagraphStyle(
        name='header',
        fontSize=16,
        spaceBefore=25,
        spaceAfter=15,
    )
    cell_header_para_style = ParagraphStyle(
        name='cell-header',
        fontSize=12,
    )
    tax_data = [
        ['Total Nights Rented: ', f'{tax_info.get_nights_rented()}'],
        ['Total Income: ', f'{"${:,.2f}".format(tax_info.get_total_income())}'],
        ['Unadjusted County Tax: ', f'{"${:,.2f}".format(tax_info.get_unadjusted_county_tax())}'],
        ['Adjusted County Tax: ', f'{"${:,.2f}".format(tax_info.get_adjusted_county_tax())}'],
        ['Unadjusted State Tax: ', f'{"${:,.2f}".format(tax_info.get_unadjusted_state_tax())}'],
        ['Adjusted State Tax: ', f'{"${:,.2f}".format(tax_info.get_adjusted_state_tax())}']
    ]
    stay_data = [
        [Paragraph('Name', style=cell_header_para_style), Paragraph('Check-In', style=cell_header_para_style), Paragraph('Check-Out', style=cell_header_para_style)],
    ]
    for stay in tax_info.get_stays():
        row = [stay.guest.name, str(stay.in_date), str(stay.out_date)]
        stay_data.append(row)
    elements = [ 
        Paragraph('Sea Prints', style=title_para_style),
        Paragraph('Tax Information', style=header_para_style),
        Table(tax_data, hAlign='LEFT'),
        Paragraph('Information calculated from the following stays: ', style=header_para_style),
        Table(stay_data, hAlign='LEFT'),
    ]
    pdf.build(elements)
    pdf_buffer.seek(0)
    return pdf_buffer

def get_filtered_stays_for_tax(postdata):
    filtered_stays = []
    for key, value in postdata.items():
        if key.startswith('in-date'):
            in_date = parser.parse(value.strip()).date()
            filtered_stays.append(Stay.objects.get(in_date=in_date))
    return filtered_stays

def register_unapproved_stay(postdata):
    '''
    When a calendar form is submitted, give the resulting request.POST data
    to this function. This function handles stripping the data down and validating/creating
    the resulting objects in the database. If the post data is validated successfully
    and the objects are created, then the returned dictionary will have a key value
    pair of 'success': True. If the validation is not successful or the objects are not
    created, then the returned dictionary will have a key value pair of 'success': False,
    and the errors will be reported in a list key value mapping of 'error_message': ['...', '...', ..]
    containing the list of error messages.
    '''
    name = postdata['name'].strip()
    age = int(postdata['age'].strip())
    phone = postdata['phone_contact_0'] + postdata['phone_contact_1'].strip()
    email = postdata['email_contact'].strip()
    num_guests = int(postdata['number_of_guests'].strip())
    in_date = parser.parse(postdata['in_date'].split('(')[0].strip())
    out_date = parser.parse(postdata['out_date'].split('(')[0].strip())
    additional = postdata['additional_questions_or_concerns']

    street = postdata['street_number'].strip()
    route = postdata['route'].strip()
    city = postdata['city'].strip()
    state = postdata['state'].strip()
    zip_code = postdata['zip_code'].strip()
    country = postdata['country'].strip()

    try:
        new_address = Address(
            street_number=street, 
            route=route, 
            city=city, 
            state=state, 
            zip_code=zip_code, 
            country=country)
        new_address.save()

        new_stay = Stay(
            name=name,
            age=age,
            in_date=in_date, 
            out_date=out_date, 
            phone_contact=phone, 
            email_contact=email, 
            number_of_guests=num_guests, 
            address=new_address, 
            additional_questions_or_concerns=additional)
        new_stay.full_clean()
        new_stay.save()


        result = {'success': True}
    except ValidationError as e:
        result = {
            'success': False,
            'error_source': 'registration.utils.register_unapproved_stay: Validation Failed',
            'error_details': e.message_dict,}
    return result

def approve_stay(stay_pk):
    try:
        target_stay = Stay.objects.get(pk=stay_pk)
        if target_stay.is_approved:
            raise ValidationError()
        target_stay.is_approved = True
        target_stay.save()
        
        result = reviews_utils.create_unpublished_review(stay_pk)
    except:
        result = {
            'success': False,
            'error_source': 'registration.utils.approve_stay: Invalid Stay Identifier',
            'error_details': {},}
    return result
