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

def home(request, year=datetime.now().year, month=datetime.now() .strftime('%B')):
    """ This is the home page """
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

def add_venue(request):
    """ This is adds a venue """
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

def show_venue(request, venue_id):
    """ This shows a venue """
    venue = Venue.objects.get(pk=venue_id)
    venue_owner = User.objects.get(pk=venue.owner)
    return render(request, 'events/show_venue.html',
    {'venue': venue,   
    'venue_owner': venue_owner})

def list_venues(request):
    """ This shows a list of venues """
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

def update_venue(request, venue_id):
    """ This updates a venue """
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(
        request.POST or None,
        request.FILES or None,
        instance=venue
    )
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/list_venues')
    else:
        form = VenueForm(instance=venue)
    
    return render(request, 'events/update_venue.html',
    {'venue': venue,
    'form': form})

# EVENTS
def all_events(request):
    """This is the list of events"""
    event_list = Event.objects.all().order_by('event_date')
    return render(request, 'events/event_list.html',
    {'event_list': event_list})

def add_event(request):
    """ This adds an event """ 
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

def update_event(request, event_id):
    """This updates an event"""
    event = Event.objects.get(pk=event_id)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list-events')

    return render(request, 'events/update_event.html',
    {'event': event,
    'form': form})

def delete_event(request, event_id):
    """This deletes an event"""
    event = Event.objects.get(pk=event_id)
    if request.user == event.manager:
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('list-events')
    else:
        messages.success(request, 'You are not authorized to delete this event!')
        return redirect('list-events')

def delete_venue(request, venue_id):
    """This deletes a venue"""
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list-venues')

def my_events(request):
    """ This shows my events """
    if request.user.is_authenticated:
        me = request.user.id
        events = Event.objects.filter(attendees=me)
        return render(request, 'events/my_events.html',
        {'events': events})
    else:
        messages.success(request, 'You are not authorized to view this page!')
        return redirect('home')

def search_events(request):
    """ This searches for an event """
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

def venue_text(request):
    """ This will generate Text File List"""
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="venue_list.txt"'
    venues = Venue.objects.all()
    for venue in venues:
        response.write(venue.name + '\n')
    return response

def venue_csv(request):
    """ This will generate Comma Separated Values (CSV) file"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="venue_list.csv"'
    writer = csv.writer(response)

    venues = Venue.objects.all()
    writer.writerow(['Venue Name', 'Address', 'Zip Code', 'Web Address', 'Phone'])
    for venue in venues:
        writer.writerow(venue.name, venue.address, venue.zip_code, venue.web, venue.phone)
    return response

def venue_pdf(request):
    """This will generate PDF file"""
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

def admin_approval(request):
    """This will approve events"""
    venue_list = Venue.objects.all()
    event_count = Event.objects.all().count()
    venue_count = Venue.objects.all().count()
    user_count = User.objects.all().count()
    event_list = Event.objects.all().order_by('-event_date')
    if request.user.is_superuser:
        if request.method == 'POST':
            for event in event_list:
                if request.POST.get('approved' + str(event.id)):
                    event.approved = True
                    event.save()
                    messages.success(request, 'Event has been approved')
                    return redirect('list-events')
                else:
                    return render(request, 'events/admin_approval.html',
                    {'event_list': event_list,
                    "event_count": event_count,
                    "venue_count": venue_count,
                    "user_count": user_count,
                    "venue_list": venue_list})
    else:
        messages.success(request, 'You are not authorized to view this page!')
        return redirect('home')

    return render(request, 'events/admin_approval.html',
                    {'event_list': event_list,
                    "event_count": event_count,
                    "venue_count": venue_count,
                    "user_count": user_count,
                    "venue_list": venue_list})

def venue_events(request, venue_id):
    """This will show venue events"""
    venue = Venue.objects.get(id=venue_id)
    events = venue.event_set.all()
    if events:
        return render(request, 'events/venue_events.html',
        {
            "events": events
        })
    else:
        messages.success(request, ("That Venue Has No Events At All!"))
        return redirect('admin-approval')
    
def show_event(request):
    """This will show an event"""
    event = Event.objects.get(pk=event_id)
    return render(request, 'events/show_event.html', 
    {'event': event})
