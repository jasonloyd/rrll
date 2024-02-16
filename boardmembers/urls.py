from django.urls import path

from . import views

app_name = "boardmembers"
urlpatterns = [
    path("", views.index, name="index"),
]