from django.urls import path

from . import views

urlpatterns = [
    path("wiki/", views.index, name="index"),
    path("<str:title>/", views.entrypage, name="entrypage"),
    path("wiki/search", views.search, name="search"),
    path("wiki/newpage", views.newpage, name="newpage"),
    path("wiki/editpage", views.editpage, name="editpage"),
    path("wiki/editsave", views.editsave, name="editsave"),
    path("wiki/randompage", views.randompage, name="randompage"),
]