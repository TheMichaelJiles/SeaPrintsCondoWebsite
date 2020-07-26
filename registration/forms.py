from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div

from phonenumber_field.widgets import PhoneNumberPrefixWidget
from phonenumber_field.formfields import PhoneNumberField

from registration.models import Stay, Address, Guest

class AddressForm(forms.ModelForm):
    class Meta():
        model = Address
        exclude = []

class GuestForm(forms.ModelForm):
    class Meta():
        model = Guest
        exclude = ["address"]


class StayForm(forms.ModelForm):
    class Meta():
        model = Stay
        exclude = ["is_approved", "is_fully_paid", "address", "total_price", "guest"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['number_of_guests'].label = '# Guests'

    in_date = forms.DateField(widget=forms.HiddenInput())
    out_date = forms.DateField(widget=forms.HiddenInput())
    phone_contact = PhoneNumberField(widget=PhoneNumberPrefixWidget())
    age = forms.IntegerField(min_value=25)
    number_of_guests = forms.IntegerField(min_value=1)

class CombinedStayAddressForm(forms.Form):
    form_classes = [GuestForm, StayForm, AddressForm]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.form_classes:
            name = f.__name__.lower()
            setattr(self, name, f(*args, **kwargs))
            form = getattr(self, name)
            self.fields.update(form.fields)
            self.initial.update(form.initial)

    def is_valid(self):
        isValid = True
        for f in self.form_classes:
            name = f.__name__.lower()
            form = getattr(self, name)
            if not form.is_valid():
                isValid = False

        if not super().is_valid():
            isValid = False
        for f in self.form_classes:
            name = f.__name__.lower()
            form = getattr(self, name)
            self.errors.update(form.errors)
        return isValid

    def clean(self):
        cleaned_data = super().clean()
        for f in self.form_classes:
            name = f.__name__.lower()
            form = getattr(self, name)
            cleaned_data.update(form.cleaned_data)
        return cleaned_data

class CombinedFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        self.layout = Layout(
            Row(
                Column('in_date', css_class='hidden-in-date-input'),
                Column('out_date', css_class='hidden-out-date-input'),
            ),
            Div(
                'name',
                'age',
                'number_of_guests',
                css_class='d-flex justify-content-between flex-wrap',
                id='personal-info-div',
            ),
            Div(
                'phone_contact',
                'email_contact',
                css_class='d-flex justify-content-between flex-wrap',
                id='contact-info-div',
            ),
            Div(
                'street_number',
                'route',
                css_class='d-flex justify-content-between flex-wrap',
                id='street-route-div',
            ),
            Div(
                'city',
                'state',
                'zip_code',
                css_class='d-flex justify-content-between flex-wrap',
                id='city-state-div',
            ),
            Div(
                'country',
                css_class='d-flex justify-content-between',
            ),
            Div(
                'additional_questions_or_concerns',
                css_class='d-flex justify-content-between',
                id='questions-div',
            ),
            Div(
                Submit('submit', 'Request Stay'),
                css_class='d-flex justify-content-center',
            )
        )
        self.render_required_fields = True
