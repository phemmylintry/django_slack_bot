from django.contrib import admin
from django.urls import path
from events.views import Events

urlpatterns = [path("admin/", admin.site.urls), path("events/", Events.as_view())]
