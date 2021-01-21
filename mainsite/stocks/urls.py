from django.urls import path

from .views import StockListView, StatisticsUSView, StatisticsListView, recent_prices

urlpatterns = [
	path('', StockListView.as_view()),
	path('stats/', StatisticsListView.as_view()),
	path('stats/usd/', StatisticsUSView.as_view()),
	path('prices/', recent_prices),
]
