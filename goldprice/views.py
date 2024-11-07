from django.shortcuts import render
from rest_framework import generics
from .models import GoldPrice
from .serializer import GoldPriceSerializer


class GoldPriceListView(generics.ListAPIView):
    queryset = GoldPrice.objects.all().order_by('-created_at')
    serializer_class = GoldPriceSerializer

