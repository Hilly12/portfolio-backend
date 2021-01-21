import sys
import pytz
import requests
import pandas as pd
from datetime import datetime
from collections import defaultdict
from stocks.models import Stock, Price, Statistics

def run():
    tickers = ['A', 'AAL', 'AAP', 'AAPL', 'ABBV', 'ABC','ABF.L', 'ABMD', 'ABT', 'ACN', 'ADANIPORTS.NS', 'ADBE', 'ADI', 'ADM', 'ADP', 'ADSK', 'AEE', 'AEP', 'AES', 'AFL', 'AHT', 'AIG', 'AIZ', 'AJG', 'AKAM', 'ALB', 'ALGN', 'ALK', 'ALL', 'ALLE', 'ALXN', 'AMAT', 'AMCR', 'AMD', 'AME', 'AMGN', 'AMP', 'AMT', 'AMZN', 'ANET', 'ANSS', 'ANTM', 'ANTO.L', 'AON', 'AOS', 'APA', 'APD', 'APH', 'APTV', 'ARE', 'ASIANPAINT.NS', 'ATO', 'ATVI', 'AUTO', 'AV.L', 'AVB', 'AVGO', 'AVST.L', 'AVV.L', 'AVY', 'AWK', 'AXISBANK.NS', 'AXP', 'AZN', 'AZO', 'BA', 'BA.L', 'BAC', 'BAJAJ-AUTO.NS', 'BAJAJFINSV.NS', 'BAJFINANCE.NS', 'BARC.L', 'BATS.L', 'BAX', 'BBY', 'BDEV.L', 'BDX', 'BEN', 'BF-B', 'BHARTIARTL.NS', 'BHP', 'BIIB', 'BIO', 'BK', 'BKG.L', 'BKNG', 'BKR', 'BLK', 'BLL', 'BLND.L', 'BME', 'BMY', 'BNZL.L', 'BP.L', 'BPCL.NS', 'BR', 'BRBY.L', 'BRITANNIA.NS', 'BRK-A', 'BSX', 'BT-A.L', 'BWA', 'BXP', 'C', 'CAG', 'CAH', 'CARR', 'CAT', 'CB', 'CBOE', 'CBRE', 'CCH.L', 'CCI', 'CCL', 'CDNS', 'CDW', 'CE', 'CERN', 'CF', 'CFG', 'CHD', 'CHRW', 'CHTR', 'CI', 'CINF', 'CIPLA.NS', 'CL', 'CLX', 'CMA', 'CMCSA', 'CME', 'CMG', 'CMI', 'CMS', 'CNC', 'CNP', 'COALINDIA.NS', 'COF', 'COG', 'COO', 'COP', 'COST', 'CPB', 'CPG', 'CPRT', 'CRDA.L', 'CRH', 'CRM', 'CSCO', 'CSX', 'CTAS', 'CTLT', 'CTSH', 'CTVA', 'CTXS', 'CVS', 'CVX', 'CXO', 'D', 'DAL', 'DCC.L', 'DD', 'DE', 'DFS', 'DG', 'DGE.L', 'DGX', 'DHI', 'DHR', 'DIS', 'DISCA', 'DISCK', 'DISH', 'DIVISLAB.NS', 'DLR', 'DLTR', 'DOV', 'DOW', 'DPZ', 'DRE', 'DRI', 'DRREDDY.NS', 'DTE', 'DUK', 'DVA', 'DVN', 'DXC', 'DXCM', 'EA', 'EBAY', 'ECL', 'ED', 'EFX', 'EICHERMOT.NS', 'EIX', 'EL', 'EMN', 'EMR', 'EOG', 'EQIX', 'EQR', 'ES', 'ESS', 'ETN', 'ETR', 'ETSY', 'EVR', 'EVRG', 'EW', 'EXC', 'EXPD', 'EXPE', 'EXPN.L', 'EXR', 'F', 'FANG', 'FAST', 'FB', 'FBHS', 'FCX', 'FDX', 'FE', 'FERG.L', 'FFIV', 'FIS', 'FISV', 'FITB', 'FLIR', 'FLS', 'FLT', 'FLTR', 'FMC', 'FOX', 'FOXA', 'FRC', 'FRES.L', 'FRT', 'FTI', 'FTNT', 'FTV', 'GAIL.NS', 'GD', 'GE', 'GILD', 'GIS', 'GL', 'GLEN.L', 'GLW', 'GM', 'GOOG', 'GPC', 'GPN', 'GPS', 'GRASIM.NS', 'GRMN', 'GS', 'GSK', 'GVC', 'GWW', 'HAL', 'HAS', 'HBAN', 'HBI', 'HCA', 'HCLTECH.NS', 'HD', 'HDFC.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS', 'HEROMOTOCO.NS', 'HES', 'HFC', 'HIG', 'HII', 'HIK.L', 'HINDALCO.NS', 'HINDUNILVR.NS', 'HL', 'HLMA.L', 'HLT', 'HOLX', 'HON', 'HPE', 'HPQ', 'HRL', 'HSBA.L', 'HSIC', 'HST', 'HSY', 'HUM', 'HWM', 'IAG', 'IBM', 'ICE', 'ICICIBANK.NS', 'ICP.L', 'IDXX', 'IEX', 'IFF', 'IHG', 'III.L', 'ILMN', 'IMB.L', 'INCY', 'INDUSINDBK.NS', 'INF.L', 'INFO', 'INFY.NS', 'INTC', 'INTU', 'IOC.NS', 'IP', 'IPG', 'IPGP', 'IQV', 'IR', 'IRM', 'ISRG', 'IT', 'ITC.NS', 'ITRK.L', 'ITW', 'IVZ', 'J', 'JBHT', 'JCI', 'JD.L', 'JET.L', 'JKHY', 'JMAT.L', 'JNJ', 'JNPR', 'JPM', 'JSWSTEEL.NS', 'K', 'KEY', 'KEYS', 'KGF.L', 'KHC', 'KIM', 'KLAC', 'KMB', 'KMI', 'KMX', 'KO', 'KOTAKBANK.NS', 'KR', 'KSU', 'L', 'LAND', 'LB', 'LDOS', 'LEG', 'LEN', 'LGEN.L', 'LH', 'LHX', 'LIN', 'LKQ', 'LLOY.L', 'LLY', 'LMT', 'LNC', 'LNT', 'LOW', 'LRCX', 'LSE.L', 'LT.NS', 'LUMN', 'LUV', 'LVS', 'LW', 'LYB', 'LYV', 'M&M.NS', 'MA', 'MAA', 'MAR', 'MARUTI.NS', 'MAS', 'MCD', 'MCHP', 'MCK', 'MCO', 'MDLZ', 'MDT', 'MET', 'MGM', 'MHK', 'MKC', 'MKTX', 'MLM', 'MMC', 'MMM', 'MNDI.L', 'MNG.L', 'MNST', 'MO', 'MOS', 'MPC', 'MRK', 'MRO', 'MRW.L', 'MS', 'MSCI', 'MSFT', 'MSI', 'MTB', 'MTD', 'MU', 'MXIM', 'NCLH', 'NDAQ', 'NEE', 'NEM', 'NESTLEIND.NS', 'NFLX', 'NG.L', 'NI', 'NKE', 'NLOK', 'NLSN', 'NOC', 'NOV', 'NOW', 'NRG', 'NSC', 'NTAP', 'NTPC.NS', 'NTRS', 'NUE', 'NVDA', 'NVR', 'NWG', 'NWL', 'NWS', 'NWSA', 'NXT.L', 'O', 'OCDO.L', 'ODFL', 'OKE', 'OMC', 'ONGC.NS', 'ORCL', 'ORLY', 'OTIS', 'OXY', 'PAYC', 'PAYX', 'PBCT', 'PCAR', 'PEAK', 'PEG', 'PEP', 'PFE', 'PFG', 'PG', 'PGR', 'PH', 'PHM', 'PHNX.L', 'PKG', 'PKI', 'PLD', 'PM', 'PNC', 'PNN.L', 'PNR', 'PNW', 'POLY.L', 'POOL', 'POWERGRID.NS', 'PPG', 'PPL', 'PRGO', 'PRU', 'PSA', 'PSH', 'PSN', 'PSON.L', 'PSX', 'PVH', 'PWR', 'PXD', 'PYPL', 'QCOM', 'QRVO', 'RB.L', 'RCL', 'RDSA.L', 'RE', 'REG', 'REGN', 'REL.L', 'RELIANCE.NS', 'RF', 'RHI', 'RIO', 'RJF', 'RL', 'RMD', 'RMV.L', 'ROK', 'ROL', 'ROP', 'ROST', 'RR.L', 'RSA.L', 'RSG', 'RTO.L', 'RTX', 'SBAC', 'SBILIFE.NS', 'SBIN.NS', 'SBRY.L', 'SBUX', 'SCHW', 'SDR.L', 'SEE', 'SGE.L', 'SGRO.L', 'SHREECEM.NS', 'SHW', 'SIVB', 'SJM', 'SKG.L', 'SLA.L', 'SLB', 'SLG', 'SMDS.L', 'SMIN', 'SMT.L', 'SN.L', 'SNA', 'SNPS', 'SO', 'SPG', 'SPGI', 'SPX.L', 'SRE', 'SSE.L', 'STAN.L', 'STE', 'STJ.L', 'STT', 'STX', 'STZ', 'SUNPHARMA.NS', 'SVT', 'SWK', 'SWKS', 'SYF', 'SYK', 'SYY', 'T', 'TAP', 'TATAMOTORS.NS', 'TATASTEEL.NS', 'TCS.NS', 'TDG', 'TDY', 'TECHM.NS', 'TEL', 'TER', 'TFC', 'TFX', 'TGT', 'TITAN.NS', 'TJX', 'TMO', 'TMUS', 'TPR', 'TROW', 'TRV', 'TSCO', 'TSLA', 'TSN', 'TT', 'TTWO', 'TW.L', 'TWTR', 'TXN', 'TXT', 'TYL', 'UA', 'UAA', 'UAL', 'UDR', 'UHS', 'ULTA', 'ULTRACEMCO.NS', 'ULVR.L', 'UNH', 'UNM', 'UNP', 'UPL.NS', 'UPS', 'URI', 'USB', 'UU.L', 'V', 'VAR', 'VFC', 'VIAC', 'VLO', 'VMC', 'VNO', 'VNT', 'VOD', 'VRSK', 'VRSN', 'VRTX', 'VTR', 'VTRS', 'VZ', 'WAB', 'WAT', 'WBA', 'WDC', 'WEC', 'WELL', 'WFC', 'WHR', 'WIPRO.NS', 'WLTW', 'WM', 'WMB', 'WMT', 'WPP', 'WRB', 'WRK', 'WST', 'WTB.L', 'WU', 'WY', 'WYNN', 'XEL', 'XLNX', 'XOM', 'XRAY', 'XRX', 'XYL', 'YUM', 'ZBH', 'ZBRA', 'ZION', 'ZTS']

    price_url = "https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1=0&period2=999999999999&interval=1d&events=history&includeAdjustedClose=true"
    stat_url = "https://query1.finance.yahoo.com/v10/finance/quoteSummary/{symbol}?modules=assetProfile,summaryProfile,summaryDetail,esgScores,price,incomeStatementHistory,incomeStatementHistoryQuarterly,balanceSheetHistory,balanceSheetHistoryQuarterly,cashflowStatementHistory,cashflowStatementHistoryQuarterly,defaultKeyStatistics,financialData,calendarEvents,secFilings,recommendationTrend,upgradeDowngradeHistory,institutionOwnership,fundOwnership,majorDirectHolders,majorHoldersBreakdown,insiderTransactions,insiderHolders,netSharePurchaseActivity,earnings,earningsHistory,earningsTrend,industryTrend,indexTrend,sectorTrend"

    failed = set()
    errors1 = defaultdict(int)
    errors2 = defaultdict(int)
    count = 0

    def get_stock_data(ticker):
        try:
            stats = requests.get(stat_url.format(symbol=ticker)).json()['quoteSummary']['result'][0]
            prices = pd.read_csv(price_url.format(symbol=ticker))
            prices.dropna(inplace=True)
            print("Retrieved Data for", ticker)
        except Exception:
            failed.add(ticker)
            print("Failed to retrieve data for", ticker)

        return stats, prices

    def get(ticker, data, *endpoints):
        d = data
        prev = 'oof'
        for endpoint in endpoints:
            if endpoint not in d:
                if endpoint == 'raw':
                    errors1[prev] += 1
                    pof = prev
                else:
                    errors2[endpoint] += 1
                    pof = endpoint
                failed.add(ticker)
                print(ticker, "failed at", f'\'{pof}\'', "endpoint")
                return None
            prev = endpoint
            d = d[endpoint]
        return d

    for ticker in tickers:
        stats, prices = get_stock_data(ticker)

        try:
            s = {
                'ticker': ticker,
                'name': get(ticker, stats, 'price', 'shortName'),
                'industry': get(ticker, stats, 'assetProfile', 'industry'),
                'country': get(ticker, stats, 'assetProfile', 'country'),
                'currency': get(ticker, stats, 'price', 'currency')
            }

            st = {
                'current_price': get(ticker, stats, 'price', 'regularMarketPrice', 'raw'),
                'market_cap': get(ticker, stats, 'price', 'marketCap', 'raw'),
                'enterprise_value': get(ticker, stats, 'defaultKeyStatistics', 'enterpriseValue', 'raw'),
                'profit_margins': get(ticker, stats, 'defaultKeyStatistics', 'profitMargins', 'raw'),
                'mean_price_200': get(ticker, stats, 'summaryDetail', 'twoHundredDayAverage', 'raw'),
                'forward_pe': get(ticker, stats, 'summaryDetail', 'forwardPE', 'raw'),
                'trailing_eps': get(ticker, stats, 'defaultKeyStatistics', 'trailingEps', 'raw'),
                'forward_eps': get(ticker, stats, 'defaultKeyStatistics', 'forwardEps', 'raw'),
                'book_value': get(ticker, stats, 'defaultKeyStatistics', 'bookValue', 'raw'),
                'price_to_book': get(ticker, stats, 'defaultKeyStatistics', 'priceToBook', 'raw'),
                'price_to_sales': get(ticker, stats, 'summaryDetail', 'priceToSalesTrailing12Months', 'raw'),
                'enterprise_to_revenue': get(ticker, stats, 'defaultKeyStatistics', 'enterpriseToRevenue', 'raw'),
                'enterprise_to_ebitda': get(ticker, stats, 'defaultKeyStatistics', 'enterpriseToEbitda', 'raw'),
                'timestamp': pytz.utc.localize(datetime.now()),
            }

            if ticker not in failed:
                stock = Stock(**s)
                stock.save()
                st['stock'] = stock
                stat = Statistics(**st)
                stat.save()
                entries = []
                for _, row in prices.iterrows():
                    p = {
                        'stock': stock,
                        'open_price': row['Open'],
                        'close_price': row['Close'],
                        'adjusted_close': row['Adj Close'],
                        'date': pytz.utc.localize(datetime.strptime(row['Date'], '%Y-%m-%d'))
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