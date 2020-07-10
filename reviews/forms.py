from django import forms
from .models import Review

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div

class ReviewForm(forms.ModelForm):
    class Meta():
        model = Review
        exclude = ['is_published', 'publish_date', 'link_key', 'corresponding_stay']
