from django.shortcuts import render
from django.http import HttpResponseRedirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Venue
from .forms import VenueForm

def home(request, year=datetime.now().year, month=datetime.now() .strftime('%B')):
    name = "Viwe Teko"
    month = month.capitalize()
    month_num = int(list(calendar.month_name).index(month))
    
    cal = HTMLCalendar().formatmonth(year, month_num)
    now = datetime.now()
    current = now.year
    time = now.strftime('%H:%M %Z%z')
    
    return render(request,
    'events/home.html', {
        "name": name,
        "year": year,
        "month": month,
        "month_num": month_num,
        "cal": cal,
        "current": current,
        "time": time,
    })

def all_events(request):
    event_list = Event.objects.all()
    return render(request, 'events/event_list.html',
    {'event_list': event_list})

def add_venue(request):
    submitted = False
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_venue.html',
    {'form': form, 'submitted': submitted})

def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    return render(request, 'events/show_venue.html',
    {'venue': venue})

def list_venues(request):
    venue_list = Venue.objects.all()
    return render(request, 'events/venue.html',
    {'venue_list': venue_list})