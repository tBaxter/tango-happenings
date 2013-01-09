from django import forms
from django.forms import ModelForm, HiddenInput, TextInput
from happenings.models import *


class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ('admin_notes', 'geocode', 'recap', 'attending', 'featured', 'related_events', 'offsite_tickets', 'ticket_sales_end')
        widgets = {
            'start_date':   TextInput(attrs={'class': 'datepicker'}),
            'end_date':     TextInput(attrs={'class': 'datepicker'}),
            'submitted_by': HiddenInput(),
            'approved':     HiddenInput(),
            'slug':         HiddenInput()
        }


class GiveawayResponseForm(ModelForm):
    class Meta:
        model = GiveawayResponse
        exclude = ('closed', 'notes')
        widgets = {
            'respondent': HiddenInput(),
            'correct': HiddenInput(),
            'question': HiddenInput(),
        }


class PlayListForm(ModelForm):
    class Meta:
        model = PlaylistItem
        exclude = ('votes')
        widgets = {
            'event': HiddenInput(),
            'user': HiddenInput(),
        }


class MemoriesForm(ModelForm):
    upload = forms.FileField(
        required=False,
        label = "Or upload your photos(s)",
        help_text='<span class="meta">You can upload one or several JPG files. Be kind, this isn\'t photobucket"</span>',
        widget=forms.FileInput(attrs={'multiple': 'multiple'})
        )
    upload_caption = forms.CharField(
        label="Caption",
        required=False,
        help_text="Note: if you are uploading multiple photos, one caption will be used.",
        widget=forms.TextInput()
    )

    class Meta:
        model = Memories
        widgets = {
            'event': HiddenInput(),
            'author': HiddenInput(),
            'photos': HiddenInput()
        }
