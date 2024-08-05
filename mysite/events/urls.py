""" This script is the urls for the events app """
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('<int:year>/<str:month>', views.home, name="home"),
    path('events/', views.all_events, name="list-events"),
    path('add_venue/', views.add_venue, name="add-venue"),
    path('list_venues/', views.list_venues, name="list-venues"),
    path('show_venue/<int:venue_id>', views.show_venue, name="show-venue"),
    path('search_venues/', views.search_venues, name="search-venues"),
    path('update_venue/<int:venue_id>', views.update_venue, name="update-venue"),
    path('add_event/', views.add_event, name="add-event"),
    path('my_events/', views.my_events, name="my-events"),
    path('search_events/', views.search_events, name="search-events"),
    path('update_event/<int:event_id>', views.update_event, name="update-event"),
    path('delete_event/<int:event_id>', views.delete_event, name="delete-event"),
    path('delete_venue/<int:venue_id>', views.delete_venue, name="delete-venue"),
    path('venue_events/<int:venue_id>', views.venue_events, name="venue-events"),
    path('show_event/<int:event_id>', views.show_event, name="show-event"),
    path('venue_text/', views.venue_text, name="venue_text"),
    path('venue_csv/', views.venue_csv, name="venue_csv"),
    path('venue_pdf/', views.venue_pdf, name="venue_pdf"),
    path('admin_approval/', views.admin_approval, name="admin-approval"),
]