from django.db.models import Model, IntegerField, FloatField, DecimalField, CharField, DateTimeField, ForeignKey, ManyToManyField, JSONField, CASCADE

class Stock(Model):
	ticker = CharField(max_length=20)
	current_price = FloatField()
	company = CharField(max_length=100)
	industry = CharField(max_length=100)
	country = CharField(max_length=60)

class Price(Model):
	stock = ForeignKey(Stock, on_delete=CASCADE)
	open_price = FloatField()
	high_price = FloatField()
	low_price = FloatField()
	close_price = FloatField()
	adjusted_close = FloatField()
	volume = IntegerField()
	date = DateTimeField()

class Statistics(Model):
	stock = ForeignKey(Stock, on_delete=CASCADE)
	market_cap = DecimalField(max_digits=20, decimal_places=2)
	enterprise_value = DecimalField(max_digits=20, decimal_places=2)
	profit_margins = FloatField()
	dividend_yield = FloatField()
	mean_price_200 = FloatField()
	trailing_pe = FloatField()
	forward_pe = FloatField()
	trailing_eps = FloatField()
	forward_eps = FloatField()
	book_value = FloatField()
	price_to_book = FloatField()
	price_to_sales = FloatField()
	enterprise_to_revenue = FloatField()
	enterprise_to_ebitda = FloatField()
	date = DateTimeField()

class BalanceSheet(Model):
	stock = ForeignKey(Stock, on_delete=CASCADE)
	cash = DecimalField(max_digits=20, decimal_places=2)
	inventory = DecimalField(max_digits=20, decimal_places=2)
	short_term_investments = DecimalField(max_digits=20, decimal_places=2)
	long_term_investments = DecimalField(max_digits=20, decimal_places=2)
	good_will = DecimalField(max_digits=20, decimal_places=2)
	total_current_assets = DecimalField(max_digits=20, decimal_places=2)
	total_current_liabilities = DecimalField(max_digits=20, decimal_places=2)
	total_assets = DecimalField(max_digits=20, decimal_places=2)
	total_liabilities = DecimalField(max_digits=20, decimal_places=2)
	total_stockholder_equity = DecimalField(max_digits=20, decimal_places=2)
	total_revenue = DecimalField(max_digits=20, decimal_places=2)
	gross_profit = DecimalField(max_digits=20, decimal_places=2)
	research_development = DecimalField(max_digits=20, decimal_places=2)
	operating_income = DecimalField(max_digits=20, decimal_places=2)
	total_operating_expenses = DecimalField(max_digits=20, decimal_places=2)
	ebit = DecimalField(max_digits=20, decimal_places=2)
	net_income = DecimalField(max_digits=20, decimal_places=2)
	date = DateTimeField()

class Index(Model):
	name = CharField(max_length=60)
	country = CharField(max_length=60)
	stocks = ManyToManyField(Stock, through='StockOnIndex')

class StockOnIndex(Model):
	stock = ForeignKey(Stock, on_delete=CASCADE)
	index = ForeignKey(Index, on_delete=CASCADE)

class UnstructuredData(Model):
	stock = ForeignKey(Stock, on_delete=CASCADE)
	data = JSONField()
