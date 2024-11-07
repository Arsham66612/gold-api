from django.urls import path
from .views import make_gapi_request

urlpatterns = [
    path('gold/', make_gapi_request)
]
