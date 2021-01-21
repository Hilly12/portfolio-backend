from django.shortcuts import render
from django.http.response import JsonResponse
from django.db.models.query import QuerySet
from django.core.serializers import serialize
from rest_framework.generics import ListAPIView
from datetime import date, timedelta
from collections import defaultdict
from .serializers import StockSerializer, StatisticsSerializer, PriceSerializer
from .models import Stock, Statistics, Price

class StockListView(ListAPIView):
	queryset = Stock.objects.all()
	serializer_class = StockSerializer

class StatisticsUSView(ListAPIView):
	queryset = Statistics.objects.filter(stock__currency='USD')
	serializer_class = StatisticsSerializer

class StatisticsListView(ListAPIView):
	queryset = Statistics.objects.all()
	serializer_class = StatisticsSerializer

def recent_prices(request):
	start_date = date.today() - timedelta(days=40)
	all_prices = Price.objects.filter(date__gte=start_date)
	prices = defaultdict(list)
	for price in serialize('python', all_prices):
		prices[price['fields']['stock']].append(price['fields'])
	return JsonResponse(prices)
	
