from os import name
from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>",views.load_page,name="load_page"),
    path("search/",views.search, name="search"),
    path("create/",views.create,name="create"),
    path("edit/<str:title>",views.edit,name="edit"),
    path("random/",views.random,name="random")
]
