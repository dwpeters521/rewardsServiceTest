from django.contrib import admin
from django.urls import path

from pointsTracker.urls import urlpatterns as tracker_urls

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += tracker_urls
