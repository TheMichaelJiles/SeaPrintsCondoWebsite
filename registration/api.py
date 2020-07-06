import registration
import home

import datetime
import pytz

def get_rates():
    seasons = []
    seasonal_objects = registration.models.SeasonPricing.objects.all()
    for obj in seasonal_objects:
        obj_dict = {
            'start': obj.start_date,
            'end': obj.end_date,
            'price': obj.price_per_night, 
        }
        seasons.append(obj_dict)
    return {
        'default': {
            'price': home.models.Globals.objects.get(pk=1).default_price_per_night,
        },
        'seasons': seasons,
    }

def get_taken_dates():
    '''
    This function looks at the database Stay data. It returns a list of
    datetime.date objects that correspond with all dates that have been taken.
    '''
    dates_taken = []
    stays = registration.models.Stay.objects.filter(is_approved=False)
    in_out_dates = set()
    for stay in stays:
        start = datetime.datetime.combine(stay.in_date, datetime.datetime.min.time()).astimezone(pytz.utc)
        end = datetime.datetime.combine(stay.out_date, datetime.datetime.min.time()).astimezone(pytz.utc)
        num_days = (end - start).days

        if start in in_out_dates:
            dates_taken.append(start)
        if end in in_out_dates:
            dates_taken.append(end)
        in_out_dates.add(start)
        in_out_dates.add(end)

        for x in range(1, num_days):
            taken_date = start + datetime.timedelta(days=x)
            dates_taken.append(taken_date)
    return dates_taken
