from tabnanny import verbose
from django.contrib.gis.db import models
import diana.abstract.models as abstract
import diana.abstract.mixins as mixins
from django.utils.translation import gettext_lazy as _

class Informant(abstract.AbstractBaseModel, mixins.GenderedMixin):

    custom_id = models.CharField(max_length=256, unique=True, blank=True, null=True, verbose_name=_("custom ID"), help_text=_("An ID of the informant provided by the researcher."))
    age = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name=_("age"), help_text=_("The approximate age of the informant."))
    note = models.TextField(null=True, blank=True, verbose_name=_("note"), help_text=_("Researcher's note on informant."))

    def __str__(self) -> str:
        return self.custom_id

class Period(abstract.AbstractTagModel):

    start_year = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name=_("start year"), help_text=_("An approximate start year, if applicable."))
    end_year = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name=_("end year"), help_text=_("An approximate end year, if applicable."))

    def __str__(self) -> str:
        return self.text

class PlaceType(abstract.AbstractTagModel):

    def __str__(self) -> str:
        return self.text

    class Meta:
        verbose_name = _("place type")
        verbose_name_plural = _("place types")

class Language(abstract.AbstractBaseModel):

    name = models.CharField(max_length=512, blank=True, null=True, verbose_name=_("name"))
    abbreviation = models.CharField(max_length=8, blank=True, null=True, verbose_name=_("abbreviation"))

    class Meta:
        verbose_name = _("language")
        verbose_name_plural = _("languages")

    def __str__(self) -> str:
        return self.name

class PlaceOfInterest(abstract.AbstractBaseModel):
    
    corrected  = models.BooleanField(default=False, verbose_name=_("corrected"))
    geometry = models.GeometryField(verbose_name=_("geometry"), blank=True, null=True)
    description = models.TextField(null=True, blank=True, verbose_name=_("description"))
    comment  = models.TextField(null=True, blank=True, verbose_name=_("comment"))
    type = models.ForeignKey(PlaceType, on_delete=models.PROTECT, verbose_name=_("type of place"), help_text=_("The type of place of interest"))

    is_iconic = models.BooleanField(default=False, verbose_name=_("is iconic"))
    is_existing = models.BooleanField(default=False, verbose_name=_("is existing"))
    is_private = models.BooleanField(default=False, verbose_name=_("is private"))

    def __str__(self) -> str:

        ns = ", ".join([f"{n.text}" for n in self.names.all()]).rstrip()

        return f"{ns}" if ns else f"{self.id}"

    class Meta:
        verbose_name = _("place of interest")
        verbose_name_plural = _("places of interest")


class Name(abstract.AbstractBaseModel):

    languages = models.ManyToManyField(Language, blank=True, verbose_name=_("language"), related_name="%(class)s_names")
    text = models.CharField(max_length=2028, blank=True, null=True, verbose_name=_("text"))
    period = models.ForeignKey(Period, null=True, blank=True, on_delete=models.PROTECT, verbose_name=_("period"), help_text=_("An approximate periodization of the name."))
    informants = models.ManyToManyField(Informant, blank=True, verbose_name=_("informants"), help_text=_("List of informants attesting to the name."), related_name="%(class)s_names")
    note = models.TextField(null=True, blank=True, verbose_name=_("note"), help_text=_("Researcher's note on the name."))
    referent = models.ForeignKey(PlaceOfInterest, on_delete=models.CASCADE, verbose_name=_("referent"), help_text=_("The street with this name."), related_name="names")

    class Meta:
        verbose_name = _("name")
        verbose_name_plural = _("names")

    def __str__(self) -> str:

        return f"{self.text}"

class Author(abstract.AbstractBaseModel):

    name = models.CharField(max_length=2028, verbose_name=_("name"))

    def __str__(self) -> str:
        return self.name

class Image(abstract.AbstractTIFFImageModel):

    title = models.CharField(max_length=1024, null=True, blank=True, verbose_name=_("general.title"))
    place_of_interest   = models.ForeignKey(PlaceOfInterest, null=True, blank=True, on_delete=models.CASCADE, related_name="images")
    description = models.TextField(null=True, blank=True)
    authors = models.ManyToManyField(Author, blank=True, related_name="images")
    informants = models.ManyToManyField(Informant, blank=True, related_name="images", verbose_name=_("informants"), help_text=_("List of informants attesting to the name."))

    def __str__(self) -> str:
        return f"{self.title}"


class Text(abstract.AbstractBaseModel):

    title = models.CharField(max_length=1024, null=True, blank=True, verbose_name=_("title"))
    place_of_interest   = models.ForeignKey(PlaceOfInterest, null=True, blank=True, on_delete=models.CASCADE, related_name="texts")
    text = models.TextField(null=True, blank=True, verbose_name=_("text"))
    authors = models.ManyToManyField(Author, blank=True, related_name="texts")
    informants = models.ManyToManyField(Informant, blank=True, related_name="texts", verbose_name=_("informants"), help_text=_("List of informants attesting to the name."))

    def __str__(self) -> str:
        return f"{self.title}"

