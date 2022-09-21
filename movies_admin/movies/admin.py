from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    extra = 1


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork


class RatingFilter(admin.SimpleListFilter):
    title = _("Rating")
    parameter_name = "rating"

    def lookups(self, request, model_admin):
        return (
            ("<5.0", "<5.0"),
            ("5.0-7.0", "5.0-7.0"),
            (">=7.0", ">=7.0"),
        )

    def queryset(self, request, queryset):
        if self.value() == "<5.0":
            return queryset.filter(
                rating__lt=5.0,
            )
        if self.value() == "5.0-7.0":
            return queryset.filter(
                rating__gte=5.0,
                rating__lt=7.0,
            )
        if self.value() == ">=7.0":
            return queryset.filter(
                rating__gte=7.0,
            )


@admin.register(Filmwork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    list_display = (
        "title",
        "type",
        "creation_date",
        "rating",
    )
    list_filter = ("type", RatingFilter)
    search_fields = (
        "title",
        "description",
        "id",
    )
    sortable_by = (
        "rating",
        "title",
    )


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = (PersonFilmworkInline,)
    list_display = ("full_name",)
    search_fields = ("full_name", "id")
