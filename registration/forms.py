from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from phonenumber_field.widgets import PhoneNumberPrefixWidget
from phonenumber_field.formfields import PhoneNumberField

from registration.models import Stay, Address

class AddressForm(forms.ModelForm):
    class Meta():
        model = Address
        exclude = []

class StayForm(forms.ModelForm):
    class Meta():
        model = Stay
        exclude = ["is_approved", "address", "total_price"]

    in_date = forms.DateField(widget=forms.HiddenInput())
    out_date = forms.DateField(widget=forms.HiddenInput())
    phone_contact = PhoneNumberField(widget=PhoneNumberPrefixWidget())

class CombinedStayAddressForm(forms.Form):
    form_classes = [StayForm, AddressForm]

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
            Row(
                Column('name', css_class='col-md-8 name-input'),
                Column('age', css_class='col-md-2 age-input'),
                Column('number_of_guests', css_class='col-md-2 number-of-guests-input'),
                css_class='name-age-num-guests-row',
            ),
            Row(
                Column('phone_contact', css_class='col-md-7 phone-contact-input'),
                Column('email_contact', css_class='col-md-5 email-contact-input'),
                css_class='mb-5 phone-email-row',
            ),
            Row(
                Column('street_number', css_class='col-md-2 street-number-input'),
                Column('route', css_class='col-md-10 route-input'),
                css_class='street-num-route-row',
            ),
            Row(
                Column('city', css_class='col-md-7 city-input'),
                Column('state', css_class='col-md-2 state-input'),
                Column('zip_code', css_class='col-md-3 zip-code-input'),
                css_class='city-state-zip-code-row',
            ),
            Row(
                Column('country', css_class='country-input'),
                css_class='mb-5 country-row',
            ),
            Row(
                Column('additional_questions_or_concerns', css_class='questions-input'),
                css_class='questions-row',
            ),
            Row(
                Submit('submit', 'Request Stay')
            )
        )
        self.render_required_fields = True
