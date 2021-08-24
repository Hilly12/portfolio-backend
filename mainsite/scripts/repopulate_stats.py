import json
import pytz
import requests
from datetime import datetime
from collections import defaultdict
from stocks.models import Statistics

max_wait = 300

stat_url = "https://query1.finance.yahoo.com/v11/finance/quoteSummary/{symbol}?modules=assetProfile,summaryProfile,summaryDetail,esgScores,price,incomeStatementHistory,incomeStatementHistoryQuarterly,balanceSheetHistory,balanceSheetHistoryQuarterly,cashflowStatementHistory,cashflowStatementHistoryQuarterly,defaultKeyStatistics,financialData,calendarEvents,secFilings,recommendationTrend,upgradeDowngradeHistory,institutionOwnership,fundOwnership,majorDirectHolders,majorHoldersBreakdown,insiderTransactions,insiderHolders,netSharePurchaseActivity,earnings,earningsHistory"


def get_stats(ticker):
    dat = None
    try:
        response = requests.get(stat_url.format(symbol=ticker))
        print(response)
        dat = response.json()["quoteSummary"]["result"][0]
        print("Retrieved data for", ticker)
    except Exception as e:
        failed.add(ticker)
        print(f"Failed to retrieve data for {ticker}; {e}")

    return dat


def get(ticker, data, *endpoints):
    d = data
    prev = "oof"
    for endpoint in endpoints:
        if endpoint not in d:
            if endpoint == "raw":
                errors1[prev] += 1
                pof = prev
            else:
                errors2[endpoint] += 1
                pof = endpoint
            failed.add(ticker)
            print(ticker, "failed at", f"'{pof}'", "endpoint")
            return None
        prev = endpoint
        d = d[endpoint]
    return d


if __name__ == "__main__":
    # t = int(random.random() * max_wait)
    # print(f"Waiting {t} seconds")
    # time.sleep(t)

    response = requests.get("https://dractal.com/stocks/").json()
    if response.status_code == 200:
        raise Exception("Unable to reach server.")

    stocks = response.json()

    failed = set()
    errors1 = defaultdict(int)
    errors2 = defaultdict(int)
    count = 0

    entries = []
    for stock in stocks:
        ticker = stock["ticker"]
        stats = get_stats(ticker)

        if not stats:
            continue

        try:
            st = {
                "stock": stock,
                "current_price": get(
                    ticker, stats, "price", "regularMarketPrice", "raw"
                ),
                "market_cap": get(ticker, stats, "price", "marketCap", "raw"),
                "enterprise_value": get(
                    ticker, stats, "defaultKeyStatistics", "enterpriseValue", "raw"
                ),
                "mean_price_200": get(
                    ticker, stats, "summaryDetail", "twoHundredDayAverage", "raw"
                ),
                "regular_market_change": get(
                    ticker, stats, "price", "regularMarketChange", "raw"
                ),
                "trailing_pe": get(ticker, stats, "summaryDetail", "trailingPE", "raw"),
                "price_to_book": get(
                    ticker, stats, "defaultKeyStatistics", "priceToBook", "raw"
                ),
                "price_to_sales": get(
                    ticker,
                    stats,
                    "summaryDetail",
                    "priceToSalesTrailing12Months",
                    "raw",
                ),
                "enterprise_to_revenue": get(
                    ticker, stats, "defaultKeyStatistics", "enterpriseToRevenue", "raw"
                ),
                "enterprise_to_ebitda": get(
                    ticker, stats, "defaultKeyStatistics", "enterpriseToEbitda", "raw"
                ),
                "timestamp": pytz.utc.localize(datetime.now()),
            }

            if ticker not in failed:
                entries.append(Statistics(**st))
                count += 1
                print("Saved data for", ticker)
        except Exception as e:
            failed.add(ticker)
            print("Failed to save data for", ticker, "with error:", e)

    Statistics.objects.all().delete()
    Statistics.objects.bulk_create(entries)

    print("Saved:", count)
    print("Failed:", failed)
    print("Errors on raw endpoint: \t", errors1)
    print("Errors on other endpoint: \t", errors2)
