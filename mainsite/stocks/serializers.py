from rest_framework.serializers import ModelSerializer

from .models import Stock, Statistics, Price, Score

class StockSerializer(ModelSerializer):
	class Meta:
		model = Stock
		fields = '__all__'

class StatisticsSerializer(ModelSerializer):
	stock = StockSerializer(read_only=True)
	
	class Meta:
		model = Statistics
		fields = '__all__'

class PriceSerializer(ModelSerializer):
	class Meta:
		model = Price
		fields = '__all__'

class ScoreSerializer(ModelSerializer):
	class Meta:
		model = Score
		fields = ('username', 'score', 'game_id')
