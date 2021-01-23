import sys
import pytz
import requests
import pandas as pd
from datetime import datetime
from collections import defaultdict
from stocks.models import Stock, Price, Statistics

def run():
	stocks = Stock.objects.all()
	failed = set()

	:
