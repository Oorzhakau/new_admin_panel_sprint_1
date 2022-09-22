from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name',)


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    autocomplete_fields = ('genre',)
    extra = 1


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ('person', 'film_work',)


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
        'get_genres',
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
    list_prefetch_related = ('genres', )

    def get_queryset(self, request):
        queryset = (
            super()
            .get_queryset(request)
            .prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    def get_genres(self, obj):
        return ', '.join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = _('Genre')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = (PersonFilmworkInline,)
    list_display = ("full_name",)
    search_fields = ("full_name", "id")
