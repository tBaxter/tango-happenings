from django.urls import path, re_path
from django.views.generic import DetailView

from .models import Update
from .views import add_event, edit_event, add_recap, create_ical, \
    EventList, EventDetail, EventsForPeriod, \
    EventUpdate, MemoryDetail, ExtraInfoDetail, event_update_list, \
    video_list, event_all_comments_list, add_attending, add_memory


# CRUD and admin functions
urlpatterns = [
    # FORMS
    path('add/', add_event, name="add_event"),
    path('<slug:slug>/edit-event/', edit_event, name="edit-event"),
    path('<slug:slug>/add-recap/', add_recap, name="add_recap"),

    # EVENT LISTS
    path('', EventList, name="events_index"),
    path('by-region/<slug:region>/', EventList, name="events_by_region"),
    path('by-state/<slug:state>/', EventList, name="events_by_state"),
    re_path(
        r'^(?P<m>\d{2})/(?P<d>\d{2})/(?P<y>\d{4})/$', 
        EventsForPeriod,
        name="events_for_day"
    ),
    re_path(
        r'^(?P<m>\d{2})/(?P<y>\d{4})/$',
        EventsForPeriod, 
        name="events_for_month"
    ),

    # ************* EVENT DETAILS *************/
    path('<slug:slug>/', EventDetail, name="event_detail"),
    path('<slug:slug>/ical/', create_ical, name="event_ical"),

    # **************** Event children ************/
    path('<slug:slug>/slides/', EventDetail, 
        {'template_name': 'happenings/event_slides.html'},
        name="event_slides"
    ),
    path('<slug:slug>/videos/', video_list, name="event_video_list"),
    path('<slug:slug>/all-comments/', event_all_comments_list, name="event_comments"),
    path('<slug:slug>/map/', EventDetail, 
        {'template_name': 'happenings/event_map.html'},
        name="event_map"
    ),
    path('<slug:slug>/attending/', EventDetail, 
        {'template_name': 'happenings/attending/list.html'},
        name='event_attending_list'
    ),
    path('<slug:slug>/attending/add/', add_attending, name="attending_add"),
    path('<slug:slug>/memories/', EventDetail, 
        {'template_name': 'happenings/memory_list.html'},
        name="event_memories"
    ),
    path('<slug:event_slug>/memories/<int:pk>/', MemoryDetail, name="memory_detail"),
    path('<slug:slug>/memories/add/', add_memory, name="add_memory"),

    # extra info pages
    path('<slug:event_slug>/extra/<slug:slug>/', ExtraInfoDetail, name="special_event_extra"),

    # updates
    path('<slug:slug>/updates/', event_update_list, name="event_update_list"),
    path('<slug:event_slug>/updates/<int:pk>/', EventUpdate, name="event_update_detail"),
    path('<slug:event_slug>/updates/<int:pk>/slides/',
        DetailView,
        {
            'template_name': "happenings/updates/update_slides.html",
            'queryset': Update.objects.all()
        },
        name="update_slides",
    ),
]
