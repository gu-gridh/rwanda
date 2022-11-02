from django.contrib.gis.db import models
from .models import *
from django.contrib.gis import admin
from diana.utils import get_fields, DEFAULT_FIELDS, DEFAULT_EXCLUDE
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import EmptyFieldListFilter

DEFAULT_LONGITUDE = -1.985070
DEFAULT_LATITUDE  = 30.031855
DEFAULT_ZOOM = 25

# class NameLanguageProxy(Name.languages.through):
#     class Meta:
#         proxy = True
#         verbose_name = _("Language in name")
#         verbose_name_plural = _("Languages in name")


#     def __str__(self):
#         return f"{self.language}"

class NyarugengeGISModelAdmin(admin.GISModelAdmin):

    default_lon = DEFAULT_LONGITUDE
    default_lat = DEFAULT_LATITUDE
    default_zoom = DEFAULT_ZOOM

    def get_name(self, obj):
        return ", ".join([f"{n.text}" for n in self.names.all()]).rstrip()

    class Meta:
        abstract = True

class BuildingNameInline(admin.TabularInline):

    model = Building.names.through

class StreetNameInline(admin.TabularInline):

    model = Street.names.through

class LanguageInline(admin.TabularInline):

    model = Name.languages.through
    extra = 1


@admin.register(Informant)
class InformantAdmin(admin.ModelAdmin):
    readonly_fields = ['id', *DEFAULT_FIELDS]
    fields = get_fields(Informant, exclude=DEFAULT_EXCLUDE)

@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    readonly_fields = ['id', *DEFAULT_FIELDS]
    fields = get_fields(Period, exclude=DEFAULT_EXCLUDE)



@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'uuid', *DEFAULT_FIELDS]
    fields = get_fields(Image, exclude=DEFAULT_EXCLUDE)


@admin.register(Street)
class StreetAdmin(NyarugengeGISModelAdmin):
    fields = get_fields(Street, exclude=DEFAULT_EXCLUDE+['names']) 
    list_display = ['id', '__str__', 'comment']
    readonly_fields = ['id', *DEFAULT_FIELDS]
    filter_horizontal = ['names']
    inlines = [StreetNameInline]
    exclude = ['names']
    search_fields = ['names__text']

@admin.register(Building)
class BuildingAdmin(NyarugengeGISModelAdmin):
    fields = get_fields(Building, exclude=DEFAULT_EXCLUDE+['names']) 
    list_display = ['id', '__str__', 'comment']
    readonly_fields = ['id', *DEFAULT_FIELDS]
    inlines = [BuildingNameInline]
    # exclude = ['names']
    search_fields = ['names__text']

# @admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    fields = get_fields(Language, exclude=DEFAULT_EXCLUDE) 
    readonly_fields = ['id', *DEFAULT_FIELDS]

@admin.register(Name)
class NameAdmin(admin.ModelAdmin):
    fields = get_fields(Name, exclude=DEFAULT_EXCLUDE+['languages']) 
    readonly_fields = ['id', *DEFAULT_FIELDS]
    inlines = [LanguageInline]
    filter_horizontal = ['informants']

