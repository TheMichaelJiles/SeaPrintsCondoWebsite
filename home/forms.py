from django import forms
from registration.models import Stay

class StayForm(forms.ModelForm):

    class Meta():
        model = Stay
        exclude = ['in_date','out_date']
        