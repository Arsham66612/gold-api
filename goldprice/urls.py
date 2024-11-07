from django.urls import path
from .views import GoldPriceListView

urlpatterns = [
    path('goldlist/', GoldPriceListView.as_view())
]
