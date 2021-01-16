from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from serializers import StockSerializer
from models import Stock

class StockViewSet(ModelViewSet):
	queryset = Stock.objects.all()
	serializer_class = StockSerializer
