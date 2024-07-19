from django import forms
from django.forms import ModelForm
from .models import Venue, Event

class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = '__all__'
        labels = {
            'name': '',
            'address': '',
            'city': '',
            'phone': '',
            'zip_code': '',
            'web': '',
            'email': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Venue Name'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'}),
            'web': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Web Address'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }


class AdminEventForm(ModelForm):
    """ This is for Admin SuperUser event form"""
    class Meta:
        model = Event
        fields = '__all__'
        labels = {
            'name': '',
            'event_date': 'YYY-MM-DD HH:MM',
            'venue': 'Venue',
            'manager': 'Manager',
            'attendees': 'Attendees',
            'description': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Name'}),
            'event_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Date'}),
            'venue': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Venue'}),
            'manager': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Manager'}),
            'attendees': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Attendees'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }

class EventForm(ModelForm):
    """ This class is the event form for ordinary users"""
    class Meta:
        model = Event
        fields = '__all__'
        labels = {
            'name': '',
            'event_date': 'YYY-MM-DD HH:MM',
            'venue': 'Venue',
            'attendees': 'Attendees',
            'description': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Name'}),
            'event_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Date'}),
            'venue': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Venue'}),
            'attendees': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Attendees'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }