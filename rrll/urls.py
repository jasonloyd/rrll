"""
URL configuration for rrll project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView
from django.urls import include, path, re_path

# from rrll import settings

from . import views

urlpatterns = [
    path("volunteers/", include("volunteers.urls")),
    path("boardmembers/", include("boardmembers.urls")),
    path("", views.index, name="index"),
    path("contact/", views.contact, name="contact"),
    path("schedule/", views.schedule, name="schedule"),
    path("safety/", views.safety, name="safety"),
    path('admin/', admin.site.urls),
    re_path(r'^favicon\.ico$',RedirectView.as_view(url='/static/assets/style/favicon.ico')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
