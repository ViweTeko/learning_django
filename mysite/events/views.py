""" This script shows the views of the events app """
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Venue
from .forms import VenueForm, EventForm, AdminEventForm
import csv
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.models import User

# HOME

""" This is the home page """
def home(request, year=datetime.now().year, month=datetime.now() .strftime('%B')):
    name = "Viwe Teko"
    month = month.capitalize()
    month_num = int(list(calendar.month_name).index(month))
    
    cal = HTMLCalendar().formatmonth(year, month_num)
    now = datetime.now()
    current = now.year
    time = now.strftime('%H:%M %Z%z')
    
    event_list = Event.objects.filter(
        event_date__year = year,
        event_date__month = month_num
        )
    return render(request,
    'events/home.html', {
        "name": name,
        "year": year,
        "month": month,
        "month_num": month_num,
        "cal": cal,
        "current": current,
        "time": time,
        "event_list": event_list,
    })

 # VENUES

""" This is adds a venue """
def add_venue(request):
    submitted = False
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id # User that's logged in
            venue.save()
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
    venue_owner = User.objects.get(pk=venue.owner)
    return render(request, 'events/show_venue.html',
    {'venue': venue,   
    'venue_owner': venue_owner})

""" This shows a list of venues """
def list_venues(request):
    venue_list = Venue.objects.all()

    p = Paginator(Venue.objects.all(), 10)
    page = request.GET.get('page')
    venue_page = p.get_page(page)
    return render(request, 'events/venue.html',
    {'venue_list': venue_list,
    'venue_page': venue_page})

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

# EVENTS
"""This is the list of events"""
def all_events(request):
    event_list = Event.objects.all().order_by('event_date')
    return render(request, 'events/event_list.html',
    {'event_list': event_list})

""" This adds an event """
def add_event(request):
    submitted = False
    if request.method == 'POST':
        if request.user.is_superuser:
            form = AdminEventForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event?submitted=True')
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user
                event.save()
                return HttpResponseRedirect('/add_event?submitted=True')
    else:
        if request.user.is_superuser:
            form = AdminEventForm()
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
    if request.user == event.manager:
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('list-events')
    else:
        messages.success(request, 'You are not authorized to delete this event!')
        return redirect('list-events')

"""This deletes a venue"""
def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list-venues')

""" This shows my events """
def my_events(request):
    if request.user.is_authenticated:
        me = request.user.id
        events = Event.objects.filter(attendees=me)
        return render(request, 'events/my_events.html',
        {'events': events})
    else:
        messages.success(request, 'You are not authorized to view this page!')
        return redirect('home')

""" This searches for an event """
def search_events(request):
    if request.POST:
        searched = request.POST['searched']
        events = Events.objects.filter(name__icontains=searched)
        return render(request, 'events/search_events.html',
        {'searched': searched,
        'events': events})
    else:
        return render(request, 'events/search_events.html',
        {})


# VENUE Downloads
""" This will generate Text File List"""
def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="venue_list.txt"'
    venues = Venue.objects.all()
    for venue in venues:
        response.write(venue.name + '\n')
    return response

""" This will generate Comma Separated Values (CSV) file"""
def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="venue_list.csv"'
    writer = csv.writer(response)
   
    venues = Venue.objects.all()
    writer.writerow(['Venue Name', 'Address', 'Zip Code', 'Web Address', 'Phone'])
    for venue in venues:
        writer.writerow(venue.name, venue.address, venue.zip_code, venue.web, venue.phone)
    return response

"""This will generate PDF file"""
def venue_pdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textobj = c.beginText()
    textobj.setTextOrigin(inch, inch)
    textobj.setFont('Helvetica', 14)
    doc = SimpleDocTemplate(buf, pagesize=letter, rightMargin=72, leftMargin=72,
    topMargin=72, bottomMargin=18)
    venues = Venue.objects.all()
    lines = []
    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email)
        lines.append(' ')

    for line in lines:
        textobj.textLine(line)
    c.drawText(textobj)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileReponse(buf, as_attachment=True, filename='venue_list.pdf')