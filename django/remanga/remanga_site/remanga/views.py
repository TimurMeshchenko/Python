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
    
    def get(self, request, *args, **kwargs):
        db_keys_different_request = {
            'types': 'manga_type',
            'rating': 'avg_rating'
        }

        different_db_table = {
            'genres': Genres.objects.all(),
            'categories': Categories.objects.all()
        }

        for url_param_key in list(request.GET.keys()): 
            url_param_values = self.request.GET.getlist(url_param_key)
            
            if bool(''.join(url_param_values)) == False:
                continue
            
            filters = self.create_url_param_filters(db_keys_different_request, url_param_key, different_db_table)
            self.filters &= filters

        return super().get(request, *args, **kwargs)

    def create_url_param_filters(self, db_keys_different_request, url_param_key, different_db_table):
        db_keys_request = url_param_key.replace("_gte", "").replace("_lte", "").replace("exclude_", "")
        db_key = db_keys_request
        url_param_values = self.request.GET.getlist(url_param_key)        
        filters = Q()
        
        for url_param_value in url_param_values:
            try:
                url_param_value = int(url_param_value)
            except:
                url_param_value = float(url_param_value)

            if db_keys_request in db_keys_different_request.keys():
                db_key = db_keys_different_request[db_keys_request]

            if "gte" in url_param_key:
                filters |= Q(**{"{}__gte".format(db_key): url_param_value})
            if "lte" in url_param_key:
                filters |= Q(**{"{}__lte".format(db_key): url_param_value})

            if db_keys_request in ['genres', 'categories']:
                Q_filter = Q(**{db_keys_request: different_db_table[db_keys_request][url_param_value]})
                
                if "exclude" in url_param_key:
                    filters &= ~Q_filter
                else:
                    filters |= Q_filter

            if db_keys_request == "types":
                Q_filter = Q(**{db_key: Title.objects.values(db_key).distinct()[url_param_value][db_key]})

                if "exclude" in url_param_key:
                    filters &= ~Q_filter
                else:
                    filters |= Q_filter

        return filters
    
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
    