from django.urls import path

from views import StockViewSet

urlpatterns = [
	path('', StockViewSet.as_view()),
]
