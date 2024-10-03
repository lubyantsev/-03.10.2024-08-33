from django import forms
from .models import Schedule, Event

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['name', 'password']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['time', 'place', 'participant_name']

class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)