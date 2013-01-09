from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic import DetailView, TemplateView

from happenings.models import *
from happenings.views import EventList, EventsForPeriod, ExtraInfoDetail, AddRecap
from shared.views import ContextDetailView

key = getattr(settings, 'GMAP_KEY', None)

urlpatterns = patterns('happenings.views',
  # CRUD and admin functions
  url(r'^add/$',  'add_event', name="add_event"),


  # EVENT LISTS
  url(r'^$', EventList.as_view(), name="events_index"),
  url(r'^by-region/(?P<region>[-\w]+)/$', EventList.as_view(), name="events_by_region"),
  url(r'^by-state/(?P<state>[-\w]+)/$', EventList.as_view(), name="events_by_state"),
  url(
    r'^(?P<m>\d{2})/(?P<d>\d{2})/(?P<y>\d{4})/$',
    EventsForPeriod.as_view(),
    name="events_for_day"
  ),
  url(
    r'^(?P<m>\d{2})/(?P<y>\d{4})/$', EventsForPeriod.as_view(), name="events_for_month"
  ),


  # ************* EVENT DETAILS *************/
  # regular calendar events
  url(
    r'^(?P<pk>\d+)/$',
    ContextDetailView.as_view(queryset=Event.objects.all(), extra_context={'key': key}),
    name='cal_event_detail'
  ),
  # special (featured events)
  url(
    r'^(?P<slug>[-\w]+)/$',
    ContextDetailView.as_view(queryset=Event.objects.all(), extra_context={'key': key}),
    name="special_event_detail"
  ),

  #url(r'^(?P<object_id>[0-9]+)/card/$', object_detail, dict(queryset=SiteUser.objects.all(), template_name="microformats/vcard.html",mimetype="text/x-vcard") ),
  # add to calendar
  url(
    r'^(?P<slug>(\w|-)+)/ical/$',
    'create_ical',
    name="event_ical"
  ),

  # slideshow
  url(
    r'^(?P<slug>(\w|-)+)/slides/$',
    DetailView.as_view(
      queryset=Event.objects.all().select_related(),
      template_name="happenings/event_slides.html"
    ),
    name="event_slides"
  ),
  url(
    r'^(?P<slug>[-\w]+)/videos/$',
    'video_list',
    name="event_video_list"
  ),

  # comments
  url(
    r'^(?P<slug>(\w|-)+)/all-comments/$',
    'event_all_comments_list',
    name="event_comments"
  ),

  # attending
  url(
    r'^(?P<slug>\d+)/attending/',
    DetailView.as_view(
      queryset=Event.objects.all(),
      template_name="happenings/attending/list.html",
      context_object_name="event",
    ),
    name='attending_list'
  ),
  url(
    r'^(?P<event_id>\d+)/attending/add/$',
    'add_attending',
    name="attending_add"
  ),

  #url(r'^(?P<event_id>\d+)/add-recap/$', AddRecap.as_view(), name="add_recap"),
  url(r'^(?P<slug>[-\w]+)/add-recap/$', AddRecap.as_view(), name="add_recap"),

  # memories
  url(
    r'^(?P<slug>[-\w]+)/memories/add/$',
    'add_memory',
    name="add_memory"
  ),
  url(
    r'^(?P<slug>(\w|-)+)/memories/',
    DetailView.as_view(
      queryset=Event.objects.all(),
      template_name="happenings/memory_list.html",
    ),
    name="event_memories"
  ),
  # extra info pages
  url(
    r'^(?P<event_slug>(\w|-)+)/extra/(?P<slug>(\w|-)+)/',
    ExtraInfoDetail.as_view(),
    name="special_event_extra"
  ),

  # update list
  url(
    r'^(?P<slug>[-\w]+)/updates/$',
    'event_update_list',
    name="event_update_list"
  ),
  # update detail
  url(
    r'^(?P<slug>[-\w]+)/updates/(?P<pk>\d+)/$',
    'event_update_detail',
    name="event_update_detail"
  ),

  # GIVEAWAYS
  url(r'^(?P<slug>[-\w]+)/giveaways/$', 'giveaways_for_event', name="giveaways"),
  url(r'^(?P<slug>[-\w]+)/giveaways/winners/$', 'giveaway_winners_for_event', name="giveaway_winner"),
  url(r'^giveaways/response/(?P<giveaway_id>\d+)/$', 'record_giveaway_response', name="giveaway_response_processing"),
  url(r'^giveaway/response-recorded/$', TemplateView.as_view(template_name="happenings/response_recorded.html"), name="giveaway_response_recorded"),

  # PLAYLIST
  url(r'^(?P<slug>[-\w]+)/playlist/$', 'playlist', name="playlist"),

)
