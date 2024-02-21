from django.urls import path

from . import views

app_name = "volunteers"
urlpatterns = [
    path("", views.home, name="home"),
    path("success", views.success, name="success"),
    path("signup", views.signup, name="signup"),
    path("volunteer_status_webhook", views.volunteer_status_webhook, name="volunteer_status_webhook"),
    path("<int:volunteer_id>", views.volunteer),
]
