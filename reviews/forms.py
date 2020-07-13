from django import forms
from .models import Review

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div

class ReviewForm(forms.ModelForm):
    class Meta():
        model = Review
        exclude = ['is_published', 'publish_date', 'link_key', 'corresponding_stay']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['review_text'].label = 'Tell us about your stay!'

    rating = forms.IntegerField(widget=forms.HiddenInput())

class ReviewFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        self.render_required_fields = True
        self.layout = Layout(
            Row(
                'rating',
                css_class = 'hidden-rating-row',
            ),
            Div(
                'review_text', 
                css_class = 'd-flex justify-content-center align-items-center',
            ),
            Div(
                Submit('submit', 'Submit Review'),
                css_class='d-flex justify-content-center align-items-center',
            ),
        )