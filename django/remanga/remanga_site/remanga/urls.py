from django.urls import path

from . import views

app_name = "remanga"
urlpatterns = [
    path("", views.CatalogView.as_view(), name="catalog"),
    path("manga/<str:dir_name>/", views.TitleView.as_view(), name="title"),
    path("search/", views.SearchView.as_view(), name="search"),
]