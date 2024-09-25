from django.contrib.gis.db import models
from .models import *
from django.contrib.gis import admin
from diana.utils import get_fields, DEFAULT_FIELDS, DEFAULT_EXCLUDE
from django.utils.translation import gettext_lazy as _
from leaflet.admin import LeafletGeoAdminMixin, LeafletGeoAdmin
from leaflet_admin_list.admin import LeafletAdminListMixin
from django.utils.html import format_html
from django.conf import settings
from leaflet_admin_list.filters import BoundingBoxFilter


DEFAULT_LONGITUDE =  30.0557
DEFAULT_LATITUDE  = -1.9397
DEFAULT_ZOOM = 12
MAX_ZOOM = 20
MIN_ZOOM = 3

class PlaceOfInterestNameInline(admin.StackedInline):

    model = Name
    fields = ('text', 'period', 'languages', 'informants', 'note',)
    autocomplete_fields = ['languages', 'informants', 'period']
    # filter_vertical = ('languages', 'informants')
    extra = 1

# admin.site.register(PlaceOfInterest, LeafletGeoAdmin)

@admin.register(PlaceOfInterest)
class PlaceOfInterestAdmin(LeafletGeoAdmin, admin.ModelAdmin,):
    display_raw = True
    fields = get_fields(PlaceOfInterest, exclude=DEFAULT_EXCLUDE) 
    list_display = ['id','__str__', 'type', 'description', 'corrected']
    readonly_fields = [*DEFAULT_FIELDS]
    autocomplete_fields = ['parent_place']
    inlines = [PlaceOfInterestNameInline]
    list_filter =('type', 'corrected', 'names__languages')
    # list_max_show_all = 600
    list_per_page = 100
    search_fields = ['names__text']
    ordering = ['names__text']

    # overrides base setting of Leaflet Geo Widget
    settings_overrides = {
       'DEFAULT_CENTER': (DEFAULT_LATITUDE, DEFAULT_LONGITUDE),
       'DEFAULT_ZOOM': DEFAULT_ZOOM,
       'MAX_ZOOM': MAX_ZOOM,
       'MIN_ZOOM': MIN_ZOOM
    }

@admin.register(Image)
class ImageModel(admin.ModelAdmin):

    fields = ['image_preview', *get_fields(Image, exclude=['id'])]
    readonly_fields = ['iiif_file', 'uuid', 'image_preview', *DEFAULT_FIELDS]
    autocomplete_fields = ['place_of_interest']
    list_display = ['thumbnail_preview', 'title', 'place_of_interest', 'uuid', 'created_at', 'updated_at']
    search_fields = ['title', 'description', 'place_of_interest__names__text']
    # ['place_of_interest__description', 'place_of_interest__comment', 'place_of_interest__names__languages__name', 'place_of_interest__names__informants__name', 'place_of_interest__names__period__text', 'place_of_interest__names__note', 'place_of_interest__type__name', 'place_of_interest__type__description', 'place_of_interest__type__comment', 'place_of_interest__type__names__text', 'place_of_interest__type__names__languages__name', 'place_of_interest__type__names__informants__name', 'place_of_interest__type__names__period__text']
    list_filter = ['place_of_interest__names__text']

    def image_preview(self, obj):
        return format_html(f'<img src="{settings.ORIGINAL_URL}/{obj.file}" height="300" />')

    def thumbnail_preview(self, obj):
        return format_html(f'<img src="{settings.ORIGINAL_URL}/{obj.file}" height="100" />')


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    readonly_fields = ['id', *DEFAULT_FIELDS]
    fields = get_fields(Text, exclude=DEFAULT_EXCLUDE)
    autocomplete_fields = ('place_of_interest',)
    search_fields = ['title', 'place_of_interest__names__text']

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    fields = get_fields(Language, exclude=DEFAULT_EXCLUDE) 
    readonly_fields = ['id', *DEFAULT_FIELDS]
    search_fields = ['name', 'abbreviation']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    readonly_fields = ['id', *DEFAULT_FIELDS]
    fields = get_fields(Author, exclude=DEFAULT_EXCLUDE)

@admin.register(Informant)
class InformantAdmin(admin.ModelAdmin):
    readonly_fields = ['id', *DEFAULT_FIELDS]
    fields = get_fields(Informant, exclude=DEFAULT_EXCLUDE)
    search_fields = ['name']

@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    readonly_fields = ['id', *DEFAULT_FIELDS]
    fields = get_fields(Period, exclude=DEFAULT_EXCLUDE)
    search_fields = ['text']

@admin.register(PlaceType)
class PlaceTypeAdmin(admin.ModelAdmin):
    fields = get_fields(PlaceType, exclude=DEFAULT_FIELDS)



@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    readonly_fields = ['id', *DEFAULT_FIELDS]
    fields = get_fields(Document, exclude=DEFAULT_EXCLUDE)
    autocomplete_fields = ('place_of_interest',)
    search_fields = ['title', 'place_of_interest__names__text']

