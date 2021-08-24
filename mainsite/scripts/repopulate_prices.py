import os
import pytz
import pandas as pd
from datetime import datetime
from stocks.models import Stock, Price

price_url = "https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1=0&period2=999999999999&interval=1d&events=history&includeAdjustedClose=true"


def run():
    failed = set()
    count = 0

    def get_prices(ticker):
        prices = None
        try:
            prices = pd.read_csv(price_url.format(symbol=ticker))
            prices.dropna(inplace=True)
            print("Retrieved data for", ticker)
        except Exception:
            print("Failed to retrieve data for", ticker)

        return prices

    try:
        scraped_tickers = open("price-bookmarks.txt", "r").read().split("\n")
    except Exception:
        scraped_tickers = []

    for stock in Stock.objects.all().iterator():
        ticker = stock.ticker

        if ticker in scraped_tickers:
            continue

        prices = get_prices(ticker)

        if prices is None:
            failed.add(ticker)
        else:
            try:
                entries = []
                for i, row in prices.iterrows():
                    p = {
                        "stock": stock,
                        "open_price": row["Open"],
                        "close_price": row["Close"],
                        "adjusted_close": row["Adj Close"],
                        "date": pytz.utc.localize(
                            datetime.strptime(row["Date"], "%Y-%m-%d")
                        ),
                    }
                    entries.append(Price(**p))

                Price.objects.bulk_create(entries, batch_size=1024)
                count += 1
                print("Saved data for", ticker)
                os.system(f"echo {ticker} >> price-bookmarks.txt")
            except Exception:
                failed.add(ticker)
                print("Failed to save data for", ticker)

    print("Saved:", count)
    print("Failed:", failed)
