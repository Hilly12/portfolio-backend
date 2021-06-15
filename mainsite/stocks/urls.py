from django.urls import path

from .views import StockListView, StatisticsListView, recent_prices, StatisticsUSView, StatisticsUKView, StatisticsIndiaView, ScoreListView

urlpatterns = [
	path('', StockListView.as_view()),
	path('stats/', StatisticsListView.as_view()),
	path('stats/usd/', StatisticsUSView.as_view()),
	path('stats/gbp/', StatisticsUKView.as_view()),
	path('stats/inr/', StatisticsIndiaView.as_view()),
	path('prices/', recent_prices),
	path('scores/', ScoreListView.as_view()),
]
