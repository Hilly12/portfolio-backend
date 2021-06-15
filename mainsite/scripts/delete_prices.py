from stocks.models import Price

def run():
	prices = Price.objects.all()
	prices.delete()
