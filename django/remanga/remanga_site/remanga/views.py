from typing import Any
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Title, Categories, Genres
from django.db.models import Q
import json

class CatalogView(generic.ListView):
    template_name = "catalog.html"
    context_object_name = "titles_list"
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.filters = Q()
        self.filter_map = dict()

    def get_queryset(self):
        return (
            Title.objects
            .order_by('-count_rating')
            .filter(self.filters)
            .distinct()
        )

    def filtration(self, request_key, object_type, all_objects=None):
        selected_values = self.request.GET.getlist(request_key)
        if selected_values != ['']:
            if not all_objects:
                all_objects = Title.objects.values(object_type).distinct()

            self.filter_map = {
                'types': lambda value: Q(**{object_type: all_objects[value][object_type]}),
                'genres': lambda value: Q(**{object_type: all_objects[value]}),
                'categories': lambda value: Q(**{object_type: all_objects[value]}),
                'issue_year_gte': lambda value: Q(issue_year__gte=value),
                'issue_year_lte': lambda value: Q(issue_year__lte=value),
                'rating_gte': lambda value: Q(avg_rating__gte=value),
                'rating_lte': lambda value: Q(avg_rating__lte=value),
                'count_chapters_gte': lambda value: Q(count_chapters__gte=value),
                'count_chapters_lte': lambda value: Q(count_chapters__lte=value),
            }

            filters = Q()
            for value in selected_values:
                try:
                    value = int(value)
                except ValueError:
                    value = float(value)

                if request_key in self.filter_map:
                    filters |= self.filter_map[request_key](value)

            self.filters &= filters

    def get(self, request, *args, **kwargs):
        self.filtration('types', 'manga_type')
        self.filtration('genres', 'genres', Genres.objects.all())
        self.filtration('categories', 'categories', Categories.objects.all())

        def call_filtration_range(request_key, object_type):
            self.filtration('{}_gte'.format(request_key), object_type)
            self.filtration('{}_lte'.format(request_key), object_type)

        call_filtration_range('issue_year','issue_year')
        call_filtration_range('rating','avg_rating')
        call_filtration_range('count_chapters','count_chapters')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        def json_dumps(variable, objects_values):
            context[variable] = json.dumps(list(objects_values)).replace('\'', '\\\'')

        json_dumps("types_data", Title.objects.values("manga_type").distinct())
        json_dumps("categories_data", Categories.objects.values())
        json_dumps("genres_data", Genres.objects.values())
        return context

class TitleView(generic.ListView):
    template_name = "title.html"
    context_object_name = "title"
    def get_queryset(self):
        title_id = self.kwargs.get('dir_name')
        return Title.objects.get(dir_name=title_id)

class SearchView(generic.ListView):
    template_name = "search.html"
    def get_queryset(self):
        return
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["json_data"] = json.dumps(list(Title.objects.values())).replace('\'', '\\\'')
        return context
    