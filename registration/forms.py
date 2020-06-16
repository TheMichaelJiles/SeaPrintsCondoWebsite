from django import forms
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from phonenumber_field.formfields import PhoneNumberField
from registration.models import Stay

class StayForm(forms.ModelForm):

    class Meta():
        model = Stay
        exclude = ["is_approved"]

    in_date = forms.DateField(widget=forms.HiddenInput())
    out_date = forms.DateField(widget=forms.HiddenInput())
    phone_contact = PhoneNumberField(widget=PhoneNumberPrefixWidget())