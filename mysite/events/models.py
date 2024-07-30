from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=100)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    phone = models.CharField('Phone Number', max_length=10)
    zip_code = models.CharField('Zip Code', max_length=10, blank=True)
    web = models.URLField('Website address', blank=True)
    email = models.EmailField('Email', blank=True)
    owner = models.IntegerField('Venue Owner', blank=False, default=1)
    venue_image = models.ImageField(null=True, blank=True, upload_to='images/')

    def __str__(self):
        return self.name


class MyClubUser(models.Model):
    first_name = models.CharField('First Name', max_length=100)
    last_name = models.CharField('Last Name', max_length=100)
    email = models.EmailField('Email', blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Event(models.Model):
    name = models.CharField('Event Name', max_length=100)
    event_date = models.DateTimeField('Event Date')
    venue = models.ForeignKey(Venue, blank=True, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, blank=True, null=True,
    on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(MyClubUser, blank=True)

    def __str__(self):
        return self.name

    @property
    def Days_till(self):
        today = date.today()
        day_of = self.event_date.date()  
        days_till = day_of - today

        days_till_stripped = str(days_till).split(',', 1)[0]
        if int(days_till) < 0:
            return print(f'{days_till_stripped} days past')

        return print(f'{days_till_stripped} days left')
