from stocks.models import Stock

def run():
	stocks = Stock.objects.all()
	stocks.delete()
