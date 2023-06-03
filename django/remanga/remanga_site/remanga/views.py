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
    
    def __init__(self, **kwargs: Any):
        self.filters = Q()

    def get_queryset(self):
        self.titles = Title.objects.order_by("-count_rating")
        self.call_filtration('types', 'manga_type', None)
        self.call_filtration('genres', 'genres', Genres.objects.all())
        self.call_filtration('categories', 'categories', Categories.objects.all())
        return self.titles

    def call_filtration(self, request_key, object_value, all_objects):
        # for i in self.request.GET.getlist(request_key):
        #     print(i)
        # print(self.request.GET.getlist(request_key))
        # print(self.request.GET.get(request_key))
        if self.request.GET.get(request_key):
        # print(self.request.GET.getlist(request_key))
        # if self.request.GET.getlist(request_key):
        #     for i in self.request.GET.getlist(request_key):
            self.filtration(request_key, object_value, all_objects)

    def filtration(self, request_key, object_value, all_objects):
        if not all_objects:
            all_objects = Title.objects.values(object_value).distinct()
        
        # def titles_filter(filter_by):
        #     print(request_key in self.request.get_full_path_info())
        #     if request_key in self.request.get_full_path_info(): #не точный
        #         self.titles = filter_by

        for index in range(len(all_objects)):
            if self.request.GET.get(request_key) == str(index):
                # titles_filter(self.titles.filter(manga_type=all_objects[index][object_value]))
                # titles_filter(self.titles.filter(genres=all_objects[index]))
                # titles_filter(self.titles.filter(categories=all_objects[index]))

                match request_key:
                    case 'types':
                        self.filters &= Q(manga_type=all_objects[index][object_value])
                        # Title.objects.order_by("-count_rating").filter(Q(manga_type=Title.objects.values('manga_type').distinct()[0]['manga_type']) 
                        # | Q(manga_type=Title.objects.values('manga_type').distinct()[1]['manga_type']))
                        # filters.append(Q(manga_type=all_objects[index][object_value]) | Q(manga_type=all_objects[1]['manga_type']))
                        # self.filters += "manga_type={} OR ".format(all_objects[index][object_value])
                        # self.filters += "manga_type={} OR ".format(all_objects[index + 1][object_value])
                        # self.titles = self.titles.filter(Q(manga_type=all_objects[index][object_value]))
                    case 'genres':
                        self.filters &= Q(genres=all_objects[index])
                        # self.filters += "genres={} OR ".format(all_objects[index])
                        # self.titles = self.titles.filter(Q(genres=all_objects[index]))
                    case 'categories':
                        self.filters &= Q(categories=all_objects[index])
                        # self.filters += "categories={} OR ".format(all_objects[index])
                        # self.titles = self.titles.filter(categories=all_objects[index])

        self.titles = self.titles.filter(self.filters)
        # self.filters_to_object()

    def filters_to_object(self):                    
        q = Q()
        self.filters = self.filters[:self.filters.rfind(' OR ')]
        for cond in self.filters.split(' OR '):
            key, value = cond.split('=')
            q |= Q(**{key: value})     
        # print(q)
        # self.titles = self.titles.filter(q)

                # if request_key == 'types':
                #     self.titles = self.titles.filter(manga_type=all_objects[index][object_value])
                # if request_key == 'genres':
                #     self.titles = self.titles.filter(genres=all_objects[index])
                # if request_key == 'categories':
                #     self.titles = self.titles.filter(categories=all_objects[index])


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
    