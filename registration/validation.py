from django.core.exceptions import ValidationError
from dateutil import parser
from .models import Stay, Address

def process_post_data(postdata):
    name = postdata['name'].strip()
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
        new_address = Address(street_number=street, route=route, city=city, state=state, zip_code=zip_code, country=country)
        new_address.save()

        new_stay = Stay(name=name, in_date=in_date, out_date=out_date, phone_contact=phone, email_contact=email, number_of_guests=num_guests, address=new_address, additional_questions_or_concerns=additional)
        new_stay.full_clean()
        new_stay.save()
        
        result = {'success': True}
    except ValidationError as e:
        result = {'success': False, 'error_message': e.messages}
    
    return result


def send_notification_email():
    raise NotImplementedError()