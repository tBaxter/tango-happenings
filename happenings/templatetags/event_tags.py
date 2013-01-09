import datetime

from django import template
from django.template import TemplateSyntaxError
from happenings.models import Event, GiveawayResponse, Update
from happenings.forms import GiveawayResponseForm

register = template.Library()


class EventsNode(template.Node):
    def __init__(self, num, varname):
        self.num, self.varname = num, varname

    def render(self, context):
        now = datetime.date.today() + datetime.timedelta(days=1)
        offset = now - datetime.timedelta(days=14)
        events = Event.objects.filter(start_date__gt=offset, featured=True).only('name', 'slug').order_by('start_date')[:self.num]
        context[self.varname] = events
        return ''


def get_events_list(parser, token):
    bits = token.contents.split()
    if len(bits) != 4:
        raise TemplateSyntaxError("get_events_list tag takes exactly three arguments")
    if bits[2] != 'as':
        raise TemplateSyntaxError("second argument to the get_events_list tag must be 'as'")
    return EventsNode(bits[1], bits[3])

get_events_list = register.tag(get_events_list)


@register.inclusion_tag('happenings/includes/past_events.html')
def load_past_events():
    today = datetime.date.today() - datetime.timedelta(days=2)
    return {'events': Event.objects.filter(start_date__lt=today, featured=True)}


@register.inclusion_tag('happenings/giveaways/giveaway_form.html')
def render_giveaway_for_update(update, giveaway):
    """
    Creates giveaway form for an update
    """
    return {
        'form': GiveawayResponseForm(),
        'giveaway': giveaway
    }


@register.inclusion_tag('happenings/giveaways/winners.html')
def render_giveaway_winners(giveaway):
    """
    shows giveaway winners
    """
    return {
        'winners': GiveawayResponse.objects.filter(question=giveaway, correct=True),
        'giveaway': giveaway
    }


@register.inclusion_tag('happenings/includes/update_pagination.html')
def paginate_update(update):
    """
    attempts to get next and previous on updates
    """
    time  = update.pub_time
    event = update.event
    try:
        next     = Update.objects.filter(event=event, pub_time__gt=time).order_by('pub_time')[0]
    except:
        next = None
    try:
        previous = Update.objects.filter(event=event, pub_time__lt=time).order_by('-pub_time')[0]
    except:
        previous = None
    return {'next': next, 'previous': previous, 'event': event}
