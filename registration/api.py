import registration

import datetime
import pytz

def get_taken_dates():
    '''
    This function looks at the database Stay data. It returns a list of
    datetime.date objects that correspond with all dates that have been taken.
    '''
    dates_taken = []
    
    #
    # Change the keyword argument of the filter() method below to 
    # is_approved=True when we are ready. Since the is_approved defaults to 
    # False when a Stay entry is created. It is easier to leave this the 
    # way it is for testing purposes. However, we actually want only approved
    # visits to appear as taken, so this will need to be changed eventually.
    #
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
