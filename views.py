import calendar
import datetime
import vobject

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.defaultfilters import slugify
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, UpdateView

from happenings.forms import GiveawayResponseForm, PlayListForm, MemoriesForm, EventForm
from happenings.models import Event, Update, Giveaway, GiveawayResponse, PlaylistItem, Image, ExtraInfo


key = getattr(settings, 'GMAP_KEY', None)


class EventList(ListView):
    """
    Returns a paginated list of events.
    """
    region = state = None
    template_name = 'happenings/index.html'
    paginate_by   = 100

    def get_queryset(self):
        now = datetime.date.today()
        offset = now - datetime.timedelta(days=10)
        events = Event.objects.filter(approved=True, start_date__gte=offset).order_by('start_date')
        if 'region' in self.kwargs:
            events = events.filter(region=self.kwargs['region'])
        return events

    #def get_context_data(self, **kwargs):
    #    context = super(EventList, self).get_context_data(**kwargs)
    #    if 'region' in kwargs:
    #        context['region'] = kwargs['region']


class EventsForPeriod(EventList):
    month = day = year = None

    def get_queryset(self, *args, **kwargs):
        qs = super(EventsForPeriod, self).get_queryset(*args, **kwargs)
        self.month = int(self.kwargs['m'])
        self.year = int(self.kwargs['y'])
        if 'd' in self.kwargs:
            self.day  = int(self.kwargs['d'])
            start_date = end_date = datetime.date(self.year, self.month, self.day)
            qs = qs.filter(start_date__lte=start_date, end_date__gte=end_date)
        else:
            start_date = datetime.date(self.year, self.month, 1)
            end_date   = datetime.date(self.year, self.month, calendar.monthrange(self.year, self.month)[1])
            qs = qs.filter(start_date__gte=start_date, end_date__lte=end_date)
        return qs

    def get_context_data(self, **kwargs):
        context = super(EventsForPeriod, self).get_context_data(**kwargs)
        if self.day:
            date = datetime.date(self.year, self.month, self.day)
            cal_type = 'day'
        else:
            date = datetime.date.strftime(datetime.date(self.year, self.month, 1), '%B %Y')
            cal_type = 'month'
        context.update({
            'cal_date' : date,
            'cal_type' : cal_type
            })
        return context


def create_ical(request, slug):
    """ Creates an ical .ics file for an event using vobject. """
    event    = get_object_or_404(Event, slug=slug)
    # convert dates to datetimes.
    # when we change code to datetimes, we won't have to do this.
    start = event.start_date
    start = datetime.datetime(start.year, start.month, start.day)

    if event.end_date:
        end = event.end_date
        end = datetime.datetime(end.year, end.month, end.day)
    else:
        end = start

    cal = vobject.iCalendar()
    cal.add('method').value = 'PUBLISH'
    vevent = cal.add('vevent')
    vevent.add('dtstart').value = start
    vevent.add('dtend').value = end
    vevent.add('dtstamp').value = datetime.datetime.now()
    vevent.add('summary').value = event.name
    response = HttpResponse(cal.serialize(), mimetype='text/calendar')
    response['Filename'] = 'filename.ics'
    response['Content-Disposition'] = 'attachment; filename=filename.ics'
    return response


def event_all_comments_list(request, slug):
    """
    Returns a list view of all comments for a given event.
    Combines event comments and update comments in one list.
    """
    event    = get_object_or_404(Event, slug=slug)
    comments = event.get_all_comments()
    is_paginated = False
    if comments:
        paginator = Paginator(comments, 50)  # Show 50 comments per page
        page = int(request.GET.get('page', 1))
        try:
            comments = paginator.page(page)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            comments = paginator.page(paginator.num_pages)
        is_paginated = comments.has_other_pages()

    return render(request, 'happenings/event_comments.html', {
        "comment_list": comments,
        "object": event,
        "page_obj": comments,
        "is_paginated": is_paginated
        }
    )


def event_update_list(request, slug):
    """
    Returns a list view of updates for a given event.
    If the event is over, it will be in chronological order.
    If the event is upcoming or still going,
    it will be in reverse chronological order.
    """
    event = get_object_or_404(Event, slug=slug)
    updates = Update.objects.filter(event__slug=slug)
    has_started = True
    if event.ended():  # if the event is over, use chronological order
        updates.order_by('id')
    else:  # if not, use reverse chronological
        updates.order_by('-id')
    return render(request, 'happenings/updates/update_list.html', {
      'event': event,
      'object_list': updates,
      'has_started': has_started,
    })


def event_update_detail(request, slug, pk):
    event  = get_object_or_404(Event, slug=slug)
    update = get_object_or_404(Update, id=pk, event=event)
    return render(request, "happenings/updates/update_detail.html", {
        'update' : update,
        'event' : event
    })


def video_list(request, slug):
    """
    Displays list of videos for given event.
    """
    event = get_object_or_404(Event, slug=slug)
    return render(request, 'video/video_list.html', {
        'event': event,
        'video_list': event.eventvideo_set.all()
    })


class ExtraInfoDetail(DetailView):
    """
    Creates a detail page for an Event.ExtraInfo, if it's not a sidebar.
    """
    queryset = ExtraInfo.objects.filter(is_sidebar=False)
    template_name = "happenings/event_extra.html"

    def dispatch(self, request, *args, **kwargs):
        self.event_slug = kwargs.get('event_slug', False)
        self.slug = kwargs.get('slug', False)
        return super(ExtraInfoDetail, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        self.event = get_object_or_404(Event, slug=self.event_slug)
        return get_object_or_404(ExtraInfo, slug=self.slug)


def giveaways_for_event(request, slug):
    event = get_object_or_404(Event, slug=slug)
    giveaways = Giveaway.objects.filter(event__slug=slug)
    return render(request, 'happenings/giveaways/giveaway_list.html', {
      'event': event,
      'giveaways': giveaways,
    })


def giveaway_winners_for_event(request, slug):
    event = get_object_or_404(Event, slug=slug)
    winners = GiveawayResponse.objects.filter(question__event__slug=slug, correct=True).order_by('respondent__id')

    template_name = 'happenings/giveaways/winners.html'
    if 'export' in request.GET:
        template_name = 'happenings/giveaways/winners_export.html'

    return render(request, template_name, {
      'event': event,
      'winners': winners,
    })


def playlist(request, slug):
    event    = get_object_or_404(Event, slug=slug)
    playlist = PlaylistItem.objects.filter(event=event).order_by('-votes')
    form = PlayListForm()
    if request.method == 'POST':
        data = request.POST.copy()
        data['user'] = request.user.id
        data['event'] = event.id
        form = PlayListForm(data, request.FILES)
        if form.is_valid():
            form.save()
    return render(request, 'happenings/playlist.html', {
      'form': form,
      'playlist_items': playlist,
      'event': event
    })





@login_required
def add_event(request):
    """ Public form to add an event. """
    approval_msg = ""
    form = EventForm()

    if request.method == 'POST':
        submission = request.POST.copy()
        submission['sites'] = settings.SITE_ID
        submission['submitted_by'] = request.user.id
        submission['approved'] = True
        submission['slug'] = slugify(submission['name'])

        form = EventForm(submission)
        if Event.objects.filter(name=submission['name'], start_date=submission['start_date']).count():
            form.errors['name'] = '<ul><li>Event is already in database</li></ul>'
        if form.is_valid():
            form.save()
            approval_msg = "Your event has successfully been submitted. "
    return render(request, 'happenings/crud/add_event.html', {'form': form, 'approval_msg': approval_msg})


class AddRecap(UpdateView):
    model = Event
    template_name = "happenings/add_recap.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AddRecap, self).dispatch(*args, **kwargs)


def add_attending(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user
    event.attending.add(user)
    event.save()
    if request.is_ajax():
        return HttpResponse(user.preferred_name, mimetype="text/html")
    return render(request, 'happenings/special_event_attending.html', {
      'obj': 'added',
      'event': event
    })


def record_giveaway_response(request, giveaway_id):
    giveaway = get_object_or_404(Giveaway, id=giveaway_id)
    form = GiveawayResponseForm()
    if request.method == 'POST':
        data = request.POST.copy()
        data['respondent'] = request.user.id
        data['question'] = giveaway.id
        # form has been submitted
        form = GiveawayResponseForm(data, request.FILES)
        if form.is_valid():
            response = form.save()
            response.respondent = request.user
            response.save()
            return HttpResponseRedirect('/happenings/giveaway/response-recorded/')
        else:
            return HttpResponse('error')
    return HttpResponseRedirect(giveaway.update_set.all()[0].get_absolute_url())


def add_memory(request, slug):
    """ Adds a memory to an event. """
    form = MemoriesForm()
    event = get_object_or_404(Event, slug=slug)

    if request.method == 'POST':
        submission = request.POST.copy()
        submission['author'] = request.user.id
        submission['event']  = event.id
        form = MemoriesForm(submission)
        if form.is_valid():
            newform = form.save()
            if request.FILES:
                for upload_file in request.FILES.getlist('upload'):
                    process_upload(upload_file, newform, form, event, request.user)
            return HttpResponseRedirect('../')
    return render(request, 'happenings/add_memories.html', {
      'form': form,
      'user': request.user
    })


def process_upload(upload_file, newform, form, event, user, status=''):
    """
    Helper function that actually processes and saves the upload(s).
    Segregated out for readability.
    """
    caption = ''
    status += "beginning upload processing. Gathering and normalizing fields....<br>"
    if 'caption' in form.cleaned_data:
        caption = form.cleaned_data['caption']
    upload_name = upload_file.name.lower()
    status += "File is %s. Checking for single file upload or bulk upload... <br>" % upload_name
    if upload_name.endswith('.jpg') or upload_name.endswith('.jpeg'):
        status += "Found jpg. Attempting to save... <br>"
        try:
            upload = Image(
              event   = event,
              image   = upload_file,
              caption = caption,
            )
            upload.save()
            newform.photos.add(upload)
            status += "Saved and uploaded jpg."
        except Exception, inst:
            status += "Error saving image: %s" % (inst)
