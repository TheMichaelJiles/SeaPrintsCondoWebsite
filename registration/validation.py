from dateutil import parser
from .models import Stay

def process_post_data(postdata):
    name = postdata['name']
    total_price = 350
    phone = postdata['phone_contact_0'] + postdata['phone_contact_1']
    email = postdata['email_contact']
    num_guests = int(postdata['number_of_guests'])
    in_date = parser.parse(postdata['in_date'].split('(')[0].strip())
    out_date = parser.parse(postdata['out_date'].split('(')[0].strip())

    if perform_validation(num_guests):
        new_stay = Stay(name=name, in_date=in_date, out_date=out_date, total_price=total_price, phone_contact=phone, email_contact=email, number_of_guests=num_guests)
        new_stay.save()
        # send_notification_email()
        is_successful = True
    else:
        is_successful = False
    return is_successful

def perform_validation(num_guests):
    return is_num_guests_valid(num_guests)

def is_num_guests_valid(num_guests):
    return num_guests > 0

def send_notification_email():
    raise NotImplementedError()