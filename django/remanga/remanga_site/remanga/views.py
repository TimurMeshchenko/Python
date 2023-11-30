from django.views import generic
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .models import *
from .forms import UserCreationForm
import json

class CatalogView(generic.ListView):
    template_name = "catalog.html"
    context_object_name = "titles_list"
    
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.filters = Q()
        self.current_filters = Q()

    def get_queryset(self):
        return (
            Title.objects
            .order_by('-count_rating')
            .filter(self.filters)
            .distinct()
        )
    
    def get(self, request, *args, **kwargs):
        self.update_filters(request)

        return super().get(request, *args, **kwargs)

    def update_filters(self, request):
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
            
            if (''.join(url_param_values) == str()): continue
            
            self.create_url_param_filters(db_keys_different_request, url_param_key, different_db_table)
            self.filters &= self.current_filters

    def create_url_param_filters(self, db_keys_different_request, url_param_key, different_db_table):
        db_keys_request = url_param_key.replace("_gte", "").replace("_lte", "").replace("exclude_", "")
        db_key = db_keys_request
        url_param_values = self.request.GET.getlist(url_param_key)        
        self.current_filters = Q()
        
        for url_param_value in url_param_values:
            try:
                url_param_value = int(url_param_value)
            except:
                url_param_value = float(url_param_value)

            if db_keys_request in db_keys_different_request.keys():
                db_key = db_keys_different_request[db_keys_request]

            self.add_range_filters(url_param_key, db_key, url_param_value)

            if db_keys_request in ['genres', 'categories']:
                Q_filter = Q(**{ db_keys_request: different_db_table[db_keys_request][url_param_value] })
                self.exclude_filter(url_param_key, Q_filter)
 
            if db_keys_request == "types":
                Q_filter = Q(**{ db_key: Title.objects.values(db_key).distinct()[url_param_value][db_key] })
                self.exclude_filter(url_param_key, Q_filter)
    
    def add_range_filters(self, url_param_key, db_key, url_param_value):
        for range_argument in ["lte", "gte"]:
            if range_argument in url_param_key:
                self.current_filters |= Q(**{f"{db_key}__{range_argument}": url_param_value})

    def exclude_filter(self, url_param_key, Q_filter):
        if "exclude" in url_param_key:
            self.current_filters &= ~Q_filter
        else:
            self.current_filters |= Q_filter
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        self.json_dumps(context, "types_data", Title.objects.values("manga_type").distinct())
        self.json_dumps(context, "categories_data", Categories.objects.values())
        self.json_dumps(context, "genres_data", Genres.objects.values())

        return context   
    
    def json_dumps(self, context, variable, objects_values):
        context[variable] = json.dumps(list(objects_values)).replace('\'', '\\\'')

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
    
class SignupView(generic.View):
    template_name = 'signup.html'

    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('/')
        
        context = { 'form': UserCreationForm() }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        context = { 'form': form }
        return render(request, self.template_name, context)

class SigninView(generic.ListView):
    template_name = "signin.html"
    
    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('/')
        
        context = { 'form': AuthenticationForm() }
        return render(request, self.template_name, context)

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('/')

        return render(request, self.template_name, {'form': form })

class LogutView(generic.ListView):
    def get(self, request):
        logout(request)
        return redirect('/')

class PasswordView(generic.ListView):
    template_name = "password.html"
    
    def get(self, request):
        if not self.request.user.is_authenticated:
            return redirect('/')
        
        context = { 'form': PasswordChangeForm(request.user) }
        return render(request, self.template_name, context)

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
                    
            return redirect('/')
        
        return render(request, self.template_name, {'form': form})
    