from rest_framework.serializers import ModelSerializer

from models import Stock

class StockSerializer(ModelSerializer):
	class Meta:
		model = Stock
		fields = '__all__'
