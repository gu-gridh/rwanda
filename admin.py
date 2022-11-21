from django.contrib.gis.db import models
from .models import *
from django.contrib.gis import admin
from diana.utils import get_fields, DEFAULT_FIELDS, DEFAULT_EXCLUDE
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import EmptyFieldListFilter
# from leaflet.admin import LeafletGeoAdminMixin
# from leaflet_admin_list.admin import LeafletAdminListMixin
from django.utils.html import format_html
from django.conf import settings

DEFAULT_LONGITUDE = -1.985070
DEFAULT_LATITUDE  = 30.031855
DEFAULT_ZOOM = 25

class NyarugengeGISModelAdmin(admin.GISModelAdmin):

    default_lon = DEFAULT_LONGITUDE
    default_lat = DEFAULT_LATITUDE
    default_zoom = DEFAULT_ZOOM

    def get_name(self, obj):
        return ", ".join([f"{n.text}" for n in self.names.all()]).rstrip()

    class Meta:
        abstract = True

class PlaceOfInterestNameInline(admin.TabularInline):

    model = Name
    fields = ('text', 'period', 'languages', 'informants', 'note',)
    filter_vertical = ('languages', 'informants')
    extra = 1

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    readonly_fields = ['id', *DEFAULT_FIELDS]
    fields = get_fields(Author, exclude=DEFAULT_EXCLUDE)

@admin.register(Informant)
class InformantAdmin(admin.ModelAdmin):
    readonly_fields = ['id', *DEFAULT_FIELDS]
    fields = get_fields(Informant, exclude=DEFAULT_EXCLUDE)

@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    readonly_fields = ['id', *DEFAULT_FIELDS]
    fields = get_fields(Period, exclude=DEFAULT_EXCLUDE)


@admin.register(Image)
class ImageModel(admin.ModelAdmin):

    fields = ['image_preview', *get_fields(Image, exclude=['id'])]
    readonly_fields = ['iiif_file', 'uuid', 'image_preview', *DEFAULT_FIELDS]
    autocomplete_fields = ['place_of_interest']
    list_display = ['thumbnail_preview', 'title', 'place_of_interest', 'uuid', 'created_at', 'updated_at']
    search_fields = ['title', 'description', 'place_of_interest']
    list_filter = ['place_of_interest']

    def image_preview(self, obj):
        return format_html(f'<img src="{settings.ORIGINAL_URL}/{obj.file}" height="300" />')

    def thumbnail_preview(self, obj):
        return format_html(f'<img src="{settings.ORIGINAL_URL}/{obj.file}" height="100" />')


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    readonly_fields = ['id', *DEFAULT_FIELDS]
    fields = get_fields(Text, exclude=DEFAULT_EXCLUDE)
    autocomplete_fields = ('place_of_interest',)

@admin.register(PlaceOfInterest)
class PlaceOfInterestAdmin(NyarugengeGISModelAdmin):
    fields = get_fields(PlaceOfInterest, exclude=DEFAULT_EXCLUDE) 
    list_display = ['id', '__str__', 'type', 'description', 'corrected']
    readonly_fields = ['id', *DEFAULT_FIELDS]
    inlines = [PlaceOfInterestNameInline]
    list_filter =('type', 'corrected', 'names__languages')
    default_zoom = 16
    search_fields = ['names__text']

# @admin.register(PlaceOfInterest)
# class PlaceOfInterestAdmin(LeafletAdminListMixin, LeafletGeoAdminMixin, admin.ModelAdmin):
#     display_raw = True
#     fields = get_fields(PlaceOfInterest, exclude=DEFAULT_EXCLUDE) 
#     list_display = ['id', '__str__', 'type', 'description', 'corrected']
#     readonly_fields = ['id', *DEFAULT_FIELDS]
#     inlines = [PlaceOfInterestNameInline]
#     list_filter =('type', 'corrected', 'names__languages')
#     list_max_show_all = 600
#     list_per_page = 600
#     default_zoom = 16
#     search_fields = ['names__text']



@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    fields = get_fields(Language, exclude=DEFAULT_EXCLUDE) 
    readonly_fields = ['id', *DEFAULT_FIELDS]

