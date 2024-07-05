""" This script shows the views of the events app """
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Venue
from .forms import VenueForm, EventForm

""" This is the home page """
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

"""This is the list of events"""
def all_events(request):
    event_list = Event.objects.all().order_by('event_date')
    return render(request, 'events/event_list.html',
    {'event_list': event_list})

""" This is adds a venue """
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

""" This shows a venue """
def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    return render(request, 'events/show_venue.html',
    {'venue': venue})

""" This shows a list of venues """
def list_venues(request):
    venue_list = Venue.objects.all()
    return render(request, 'events/venue.html',
    {'venue_list': venue_list})

""" This searches for a venue """
def search_venues(request):
    if request.POST:
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__icontains=searched)
        return render(request, 'events/search_venues.html',
        {'searched': searched,
        'venues': venues})
    else:
        return render(request, 'events/search_venues.html',
        {})

""" This updates a venue """
def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, instance=venue)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/list_venues')
    else:
        form = VenueForm(instance=venue)
    
    return render(request, 'events/update_venue.html',
    {'venue': venue,
    'form': form})


""" This adds an event """
def add_event(request):
    submitted = False
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_event?submitted=True')
    else:
        form = EventForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_event.html',
    {'form': form, 'submitted': submitted})

"""This updates an event"""
def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list-events')

    return render(request, 'events/update_event.html',
    {'event': event,
    'form': form})

"""This deletes an event"""
def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return redirect('list-events')

"""This deletes a venue"""
def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list-venues')