from registration.models import Stay
import datetime

def get_taken_dates():
    dates_taken = []
    stays = Stay.objects.all()
    for stay in stays:
        start = stay.in_date
        end = stay.out_date
        num_days = (end - start).days
        for x in range(1, num_days):
            taken_date = start + datetime.timedelta(days=x)
            dates_taken.append(str(taken_date))
    return dates_taken
