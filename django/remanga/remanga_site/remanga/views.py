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
    
    # def __init__(self, **kwargs: Any):
    #     self.filters = Q()

    # def get_queryset(self):
    #     self.titles = Title.objects.order_by("-count_rating")
    #     self.filtration('types', 'manga_type', None)
    #     self.filtration('genres', 'genres', Genres.objects.all())
    #     self.filtration('categories', 'categories', Categories.objects.all())
    #     return self.titles

    # def filtration(self, request_key, object_value, all_objects):
    #     if self.request.GET.getlist(request_key):
    #         if not all_objects:
    #             all_objects = Title.objects.values(object_value).distinct()

    #         for index in self.request.GET.getlist(request_key):
    #             index = int(index)
    #             if len(self.request.GET.getlist(request_key)) == 1:
    #                 match request_key:
    #                     case 'types':
    #                         self.filters &= Q(manga_type=all_objects[index][object_value])
    #                     case 'genres':
    #                         self.filters &= Q(genres=all_objects[index])
    #                     case 'categories':
    #                         self.filters &= Q(categories=all_objects[index])
    #             else:
    #                 match request_key:
    #                     case 'types':
    #                         self.filters |= Q(manga_type=all_objects[index][object_value])
    #                     case 'genres':
    #                         self.filters |= Q(genres=all_objects[index])
    #                     case 'categories':
    #                         self.filters |= Q(categories=all_objects[index])  
            
    #         self.titles = self.titles.filter(self.filters).distinct()


    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.filters = Q()

    def get_queryset(self):
        return (
            Title.objects
            .order_by('-count_rating')
            .filter(self.filters)
            .distinct()
        )

    def filtration(self, request_key, object_value, all_objects=None):
        selected_values = self.request.GET.getlist(request_key)
        if selected_values:
            if not all_objects:
                all_objects = Title.objects.values(object_value).distinct()

            filters = Q()
            for index in selected_values:
                index = int(index)
                if request_key == 'types':
                    kwargs = {object_value: all_objects[index][object_value]}
                else:
                    kwargs = {object_value: all_objects[index]}
                filters |= Q(**kwargs)
            self.filters &= filters

    def get(self, request, *args, **kwargs):
        self.filtration('types', 'manga_type')
        self.filtration('genres', 'genres', Genres.objects.all())
        self.filtration('categories', 'categories', Categories.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories_data"] = json.dumps(list(Categories.objects.values())).replace('\'', '\\\'')
        context["genres_data"] = json.dumps(list(Genres.objects.values())).replace('\'', '\\\'')
        context["types_data"] = json.dumps(list(Title.objects.values("manga_type").distinct())).replace('\'', '\\\'')
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
        return 0
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["json_data"] = json.dumps(list(Title.objects.values())).replace('\'', '\\\'')
        return context
    