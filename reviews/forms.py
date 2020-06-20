from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta():
        model = Review
        exclude = ['is_published', 'publish_date', 'link_key', 'corresponding_stay']
