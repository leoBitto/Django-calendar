# forms.py

from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'start_date', 'start_time', 'end_date', 'end_time', 'description']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError('Start date must be before the end date.')

        if start_date == end_date and start_time and end_time and start_time >= end_time:
            raise forms.ValidationError('Start time must be before the end time when the dates are the same.')
