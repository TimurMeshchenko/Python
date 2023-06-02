from django.shortcuts import render
from django.http import Http404, HttpResponse

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Title

import json

class CatalogView(generic.ListView):
    template_name = "catalog.html"
    context_object_name = "titles_list"
    def get_queryset(self):
        return Title.objects.order_by("-count_rating")[:31]

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
    