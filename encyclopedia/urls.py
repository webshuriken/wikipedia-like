from django.urls import path

from . import views

app_name = 'encyclopedia'
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("wiki/entry-not-found", views.entry_not_found, name="entry_not_found"),
    path("new-page", views.new_page, name="new-page"),
    path("edit-page", views.edit_page, name="edit-page"),
    path("edit-page/<str:entry>", views.edit_page, name="edit-page"),
    path("random", views.random, name="random-page")
]
