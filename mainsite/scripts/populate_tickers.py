import sys
import pytz
import requests
import pandas as pd
from datetime import datetime
from collections import defaultdict
from stocks.models import Stock, Price, Statistics


def run():
    # tickers = ['SNA', 'SNPS', 'SO', 'SPG', 'SPGI', 'SPX.L', 'SRE', 'SSE.L', 'STAN.L', 'STE', 'STJ.L', 'STT', 'STX', 'STZ', 'SUNPHARMA.NS', 'SVT', 'SWK', 'SWKS', 'SYF', 'SYK', 'SYY', 'T', 'TAP', 'TATAMOTORS.NS', 'TATASTEEL.NS', 'TCS.NS', 'TDG', 'TDY', 'TECHM.NS', 'TEL', 'TER', 'TFC', 'TFX', 'TGT', 'TITAN.NS', 'TJX', 'TMO', 'TMUS', 'TPR', 'TROW', 'TRV', 'TSCO', 'TSLA', 'TSN', 'TT', 'TTWO', 'TW.L', 'TWTR', 'TXN', 'TXT', 'TYL', 'UA', 'UAA', 'UAL', 'UDR', 'UHS', 'ULTA', 'ULTRACEMCO.NS', 'ULVR.L', 'UNH', 'UNM', 'UNP', 'UPL.NS', 'UPS', 'URI', 'USB', 'UU.L', 'V', 'VAR', 'VFC', 'VIAC', 'VLO', 'VMC', 'VNO', 'VNT', 'VOD', 'VRSK', 'VRSN', 'VRTX', 'VTR', 'VTRS', 'VZ', 'WAB', 'WAT', 'WBA', 'WDC', 'WEC', 'WELL', 'WFC', 'WHR', 'WIPRO.NS', 'WLTW', 'WM', 'WMB', 'WMT', 'WPP', 'WRB', 'WRK', 'WST', 'WTB.L', 'WU', 'WY', 'WYNN', 'XEL', 'XLNX', 'XOM', 'XRAY', 'XRX', 'XYL', 'YUM', 'ZBH', 'ZBRA', 'ZION', 'ZTS']
    tickers = ["ULVR.L", "SNOW"]
    price_url = "https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1=0&period2=999999999999&interval=1d&events=history&includeAdjustedClose=true"
    stat_url = "https://query1.finance.yahoo.com/v10/finance/quoteSummary/{symbol}?modules=assetProfile,summaryProfile,summaryDetail,esgScores,price,incomeStatementHistory,incomeStatementHistoryQuarterly,balanceSheetHistory,balanceSheetHistoryQuarterly,cashflowStatementHistory,cashflowStatementHistoryQuarterly,defaultKeyStatistics,financialData,calendarEvents,secFilings,recommendationTrend,upgradeDowngradeHistory,institutionOwnership,fundOwnership,majorDirectHolders,majorHoldersBreakdown,insiderTransactions,insiderHolders,netSharePurchaseActivity,earnings,earningsHistory,earningsTrend,industryTrend,indexTrend,sectorTrend"

    failed = set()
    errors1 = defaultdict(int)
    errors2 = defaultdict(int)
    count = 0

    def get_stock_data(ticker):
        try:
            stats = requests.get(stat_url.format(symbol=ticker)).json()["quoteSummary"][
                "result"
            ][0]
            prices = pd.read_csv(price_url.format(symbol=ticker))
            prices.dropna(inplace=True)
            print("Retrieved Data for", ticker)
        except Exception:
            failed.add(ticker)
            print("Failed to retrieve data for", ticker)

        return stats, prices

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

    for ticker in tickers:
        stats, prices = get_stock_data(ticker)

        try:
            s = {
                "ticker": ticker,
                "name": get(ticker, stats, "price", "shortName"),
                "industry": get(ticker, stats, "assetProfile", "industry"),
                "country": get(ticker, stats, "assetProfile", "country"),
                "currency": get(ticker, stats, "price", "currency"),
            }

            st = {
                "current_price": get(
                    ticker, stats, "price", "regularMarketPrice", "raw"
                ),
                "market_cap": get(ticker, stats, "price", "marketCap", "raw"),
                "enterprise_value": get(
                    ticker, stats, "defaultKeyStatistics", "enterpriseValue", "raw"
                ),
                "profit_margins": get(
                    ticker, stats, "defaultKeyStatistics", "profitMargins", "raw"
                ),
                "mean_price_200": get(
                    ticker, stats, "summaryDetail", "twoHundredDayAverage", "raw"
                ),
                "trailing_pe": get(ticker, stats, "summaryDetail", "trailingPE", "raw"),
                "trailing_eps": get(
                    ticker, stats, "defaultKeyStatistics", "trailingEps", "raw"
                ),
                "forward_eps": get(
                    ticker, stats, "defaultKeyStatistics", "forwardEps", "raw"
                ),
                "book_value": get(
                    ticker, stats, "defaultKeyStatistics", "bookValue", "raw"
                ),
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
                stock = Stock(**s)
                stock.save()
                st["stock"] = stock
                stat = Statistics(**st)
                stat.save()
                entries = []
                for _, row in prices.iterrows():
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
                Price.objects.bulk_create(entries)
                count += 1
                print("Saved data for", ticker)
        except Exception as e:
            failed.add(ticker)
            print("Failed to save data for", ticker, "with error:", e)

    print("Saved", count)
    print("Failed:", failed)
    print("Errors on raw endpoint: \t", errors1)
    print("Errors on other endpoint: \t", errors2)
