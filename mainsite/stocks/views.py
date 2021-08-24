from django.shortcuts import render
from django.http.response import JsonResponse
from django.db.models.query import QuerySet
from django.core.serializers import serialize
from rest_framework.generics import ListAPIView
from datetime import datetime, timedelta, timezone
from collections import defaultdict
from .serializers import (
    StockSerializer,
    StatisticsSerializer,
    PriceSerializer,
    ScoreSerializer,
    BlogSerializer,
)
from .models import Stock, Statistics, Price, Score, Blog


class StockListView(ListAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class StatisticsUSView(ListAPIView):
    queryset = Statistics.objects.filter(stock__currency="USD")
    serializer_class = StatisticsSerializer


class StatisticsUKView(ListAPIView):
    queryset = Statistics.objects.filter(stock__currency="GBp")
    serializer_class = StatisticsSerializer


class StatisticsIndiaView(ListAPIView):
    queryset = Statistics.objects.filter(stock__currency="INR")
    serializer_class = StatisticsSerializer


class StatisticsListView(ListAPIView):
    queryset = Statistics.objects.all()
    serializer_class = StatisticsSerializer


def recent_prices(request):
    start_date = datetime.now(timezone.utc) - timedelta(days=180)
    all_prices = Price.objects.filter(date__gte=start_date)
    prices = defaultdict(list)
    for price in serialize("python", all_prices):
        prices[price["fields"]["stock"]].append(
            {
                "price": price["fields"]["adjusted_close"],
                "date": (price["fields"]["date"] - start_date).days,
            }
        )
    return JsonResponse(prices)


class ScoreListView(ListAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer


class BlogListView(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
