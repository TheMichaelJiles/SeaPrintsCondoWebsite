from models import Stay
import datetime

def add_stay(name, checkin, checkout, price, phone, email, number_of_guests=1):
    new_stay = Stay(name=name, in_date=checkin, out_date=checkout, total_price=price, phone_contact=phone, email_contact=email, number_of_guests=number_of_guests)
    new_stay.save()

def remove_stay(name):
    Stay.objects.filter(name=name).delete()

def get_dates_taken():
    dates_taken = []
    stays = Stay.objects.all()
    for stay in stays:
        start = stay.in_date
        end = stay.out_date
        num_days = (end - start).days
        for x in range(num_days):
            taken_date = start + datetime.timedelta(days=x)
            dates_taken.append(taken_date)
    return dates_taken

def get_all_stays():
    return [StayDetails(stay) for stay in Stay.objects.all()]

class StayDetails:
    def __init__(self, stay_obj):
        self._stay_obj = stay_obj

    def get_name(self):
        return self._stay_obj.name
    
    def get_checkin(self):
        return self._stay_obj.in_date

    def get_checkout(self):
        return self._stay_obj.out_date

    def get_total_price(self):
        return self._stay_obj.total_price

    def get_phone_contact(self):
        return self._stay_obj.phone_contact

    def get_email_contact(self):
        return self._stay_obj.email_contact

    def get_number_of_guests(self):
        return self._stay_obj.number_of_guests
