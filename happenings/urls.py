from django.conf.urls import patterns, url
from django.views.generic import DetailView, TemplateView

from .models import Update
from .views import EventDetail, EventUpdate, MemoryDetail, ExtraInfoDetail


# CRUD and admin functions
urlpatterns = patterns(
    'happenings.views',
    url(
        regex=r'^add/$',
        view='add_event',
        name="add_event"
    ),
    url(
        regex=r'^(?P<slug>[-\w]+)/edit-event/$',
        view='edit_event',
        name="edit-event"
    ),
    url(
        regex=r'^(?P<slug>[-\w]+)/add-recap/$',
        view='add_recap',
        name="add_recap"
    ),

    # EVENT LISTS
    url(
        name="events_index",
        regex=r'^$',
        view='event_list'
    ),
    url(
        name="events_by_region",
        regex=r'^by-region/(?P<region>[-\w]+)/$',
        view='event_list'
    ),
    url(
        name="events_by_state",
        regex=r'^by-state/(?P<state>[-\w]+)/$',
        view='event_list'
    ),
    url(
        name="events_for_day",
        regex=r'^(?P<m>\d{2})/(?P<d>\d{2})/(?P<y>\d{4})/$',
        view='events_for_period'
    ),
    url(
        name="events_for_month",
        regex=r'^(?P<m>\d{2})/(?P<y>\d{4})/$',
        view='events_for_period',
    ),

    # ************* EVENT DETAILS *************/
    url(
        name="event_detail",
        regex=r'^(?P<slug>[-\w]+)/$',
        view='event_detail',
    ),

    # add to calendar
    url(
        name="event_ical",
        regex=r'^(?P<slug>[-\w]+)/ical/$',
        view='create_ical',
    ),

    # **************** Event children ************/
    # slideshow
    url(
        name="event_slides",
        regex=r'^(?P<slug>[-\w]+)/slides/$',
        view=EventDetail.as_view(template_name="happenings/event_slides.html"),
    ),
    # videos
    url(
        name="event_video_list",
        regex=r'^(?P<slug>[-\w]+)/videos/$',
        view='video_list',
    ),
    url(
        name="event_comments",
        regex=r'^(?P<slug>(\w|-)+)/all-comments/$',
        view='event_all_comments_list',
    ),
)

# Special cases and event children
urlpatterns += patterns(
    '',
    # slideshow
    url(
        name="event_slides",
        regex=r'^(?P<slug>[-\w]+)/slides/$',
        view=EventDetail.as_view(template_name="happenings/event_slides.html"),
    ),
    # map
    url(
        name="event_map",
        regex=r'^(?P<slug>[-\w]+)/map/$',
        view=EventDetail.as_view(template_name="happenings/event_map.html"),
    ),
    # attending
    url(
        name='event_attending_list',
        regex=r'^(?P<slug>[-\w]+)/attending/$',
        view=EventDetail.as_view(template_name="happenings/attending/list.html"),
    ),
    url(
        name="attending_add",
        regex=r'^(?P<slug>[-\w]+)/attending/add/$',
        view='happenings.views.add_attending',
    ),
    # memories
     url(
        name="event_memories",
        regex=r'^(?P<slug>(\w|-)+)/memories/$',
        view=EventDetail.as_view(template_name="happenings/memory_list.html"),
    ),
    url(
        name="memory_detail",
        regex=r'^(?P<event_slug>(\w|-)+)/memories/(?P<pk>\d+)/',
        view=MemoryDetail.as_view(),
    ),
    url(
        name="add_memory",
        regex=r'^(?P<slug>[-\w]+)/memories/add/$',
        view='happenings.views.add_memory',
    ),

    # extra info pages
    url(
        name="special_event_extra",
        regex=r'^(?P<event_slug>(\w|-)+)/extra/(?P<slug>(\w|-)+)/',
        view=ExtraInfoDetail.as_view(),
    ),

    # update list
    url(
        name="event_update_list",
        regex=r'^(?P<slug>[-\w]+)/updates/$',
        view='happenings.views.event_update_list',
    ),

    # update detail
    url(
        name="event_update_detail",
        regex=r'^(?P<event_slug>(\w|-)+)/updates/(?P<pk>\d+)/$',
        view=EventUpdate.as_view(),
    ),
    url(
        regex=r'^(?P<event_slug>(\w|-)+)/updates/(?P<pk>\d+)/slides/$',
        name="update_slides",
        view=DetailView.as_view(
            queryset=Update.objects.all(),
            template_name="happenings/updates/update_slides.html",
        )
    ),

    # GIVEAWAYS
    url(
        name="giveaways",
        regex=r'^(?P<slug>[-\w]+)/giveaways/$',
        view='happenings.views.giveaways_for_event',
    ),
    url(
        name="giveaway_winner",
        regex=r'^(?P<slug>[-\w]+)/giveaways/winners/$',
        view='happenings.views.giveaway_winners_for_event',
    ),
    url(
        name="giveaway_response_processing",
        regex=r'^giveaways/(?P<giveaway_id>\d+)/response/$',
        view='happenings.views.record_giveaway_response',
    ),
    url(
        name="giveaway_response_recorded",
        regex=r'^giveaway/response-recorded/$',
        view=TemplateView.as_view(template_name="happenings/response_recorded.html"),
    ),
)
