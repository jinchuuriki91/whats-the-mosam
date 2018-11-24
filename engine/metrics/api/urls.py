from . import rest
from django.urls import path, re_path


urlpatterns = [
    path('metric/', rest.MetricsHandler.as_view())
]