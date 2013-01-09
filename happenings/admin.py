from django.contrib import admin
from happenings.models import *


class ExtraInfoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class ExtraInfoInline(admin.StackedInline):
    model = ExtraInfo
    extra = 1


class ImageInline(admin.TabularInline):
    model = Image
    extra = 3


class EventBulkInline(admin.TabularInline):
    model   = BulkEventImageUpload
    max_num = 1


class UpdateImageInline(admin.TabularInline):
    model = UpdateImage
    extra = 6


class GiveawayResponseInline(admin.TabularInline):
    model = GiveawayResponse


class GiveawayInline(admin.TabularInline):
    model = Giveaway
    extra = 1


class VideoInline(admin.TabularInline):
    model = EventVideo
    extra = 1


class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 3


class GiveawayAdmin(admin.ModelAdmin):
    date_hierarchy      = 'pub_time'
    list_display        = ('question', 'prize', 'event', 'closed',)
    list_filter         = ('closed', 'event')
    inlines = [
        GiveawayResponseInline,
    ]
    fieldsets = (
      ('', {'fields': ('event', )}),
      ('Q and A', {'fields': ('question', 'long_q', 'explanation')}),
      ('For', {'fields': (('number', 'prize'), 'closed', )}),
    )


class EventAdmin(admin.ModelAdmin):
    search_fields       = ['name', ]
    list_display        = ('name', 'approved', 'featured', 'submitted_by', 'start_date',)
    list_filter         = ('featured', 'region')
    date_hierarchy      = 'start_date'
    filter_horizontal   = ('attending', 'related_events')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [
        ImageInline,
        EventBulkInline,
        VideoInline,
        ExtraInfoInline,
        ScheduleInline,
    ]
    fieldsets = (
        ('General info', {'fields': ('name', 'featured', 'info', 'recap', 'related_events')}),
        ('Dates', {'fields': ('start_date', 'end_date',)}),
        ('Venue/Location', {'fields': ('region', 'venue', 'address', 'city', 'state', 'zipcode', 'website', 'phone', )}),
        ('Ticketing', {'fields': ('offsite_tickets', 'ticket_sales_end'), 'classes': ['collapse']}),
        ('Staff info', {'fields': ('submitted_by', 'admin_notes', 'approved', 'geocode', 'slug'), 'classes': ['collapse']}),
    )


class UpdateAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_time',)
    list_filter = ('event',)
    filter_horizontal = ('giveaway',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'author':
            kwargs['initial'] = request.user.id
            return db_field.formfield(**kwargs)
        if db_field.name == 'event':
            kwargs['initial'] = Event.objects.filter(featured=True).latest('id')
            return db_field.formfield(**kwargs)
        return super(UpdateAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    inlines = [
        UpdateImageInline,
    ]

admin.site.register(Event, EventAdmin)
admin.site.register(Update, UpdateAdmin)
admin.site.register(ExtraInfo, ExtraInfoAdmin)
admin.site.register(Giveaway, GiveawayAdmin)
admin.site.register(PlaylistItem)
admin.site.register(Memories)
