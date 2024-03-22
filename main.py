from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest
import config
import requests
from yahoo_fin import stock_info


class StockPortfolio:
    def __init__(self, nameOfPortfolio):
        self.nameOfPortfolio = nameOfPortfolio
        self.numOfStock = 0
        self.stockInfo = {}
        dictOfStocks = getPositionInfo()

        for stock in dictOfStocks.keys():
            qty = dictOfStocks[stock]['qty']
            price = dictOfStocks[stock]['avg_entry_price']
            self.addstock(stock, float(qty), float(price))

    def addstock(self, stock_name, num_of_shares, cost_per_share):
        if stock_name not in self.stockInfo:
            self.stockInfo[stock_name] = {
                'qty': num_of_shares,
                'avg_entry_price': cost_per_share
            }
        else:
            self.stockInfo[stock_name]['qty'] += num_of_shares
            self.stockInfo[stock_name]['avg_entry_price'] = getPositionInfo()[stock_name]['avg_entry_price']

        self.numOfStock += 1
    # def sellStock(self, stock_name, num_of_shares, cost_per_share):

    def stockCount(self):
        return self.numOfStock

    def printstocks(self):
        print(self.stockInfo)

    def deletestock(self, deleted_stock):
        if deleted_stock in self.stockInfo:
            del self.stockInfo[deleted_stock]
        else:
            print("This item is not in your portfolio.")

    def clear(self):
        self.numOfStock = 0
        self.stockInfo = {}


def getStockPrice(stock):
    return stock_info.get_live_price(stock)


def getPositionInfo():
    url = "https://paper-api.alpaca.markets/v2/positions"

    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": config.API_KEY,
        "APCA-API-SECRET-KEY": config.SECRET_KEY
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()  # Parse response JSON
        result = {}

        for position in data:
            symbol = position['symbol']
            qty = position['qty']
            avg_entry_price = position['avg_entry_price']

            result[symbol] = {
                'qty': qty,
                'avg_entry_price': avg_entry_price
            }

        return result
    else:
        print("Failed to fetch position information:", response.text)
        return None


def buyStocks(tradingClient, stock, qty, side, time_in_force, NamePortfolio):
    order_details = MarketOrderRequest(
        symbol=stock,
        qty=qty,
        side=side,
        time_in_force=time_in_force
    )

    order = tradingClient.submit_order(order_data=order_details)
    NamePortfolio.addstock(stock, qty, getStockPrice(stock))

def sellStocks(tradingClient, stock, qty, side, time_in_force, NamePortfolio):
    order_details = MarketOrderRequest(
        symbol=stock,
        qty=qty,
        side=side,
        time_in_force=time_in_force
    )

    order = tradingClient.submit_order(order_data=order_details)
    NamePortfolio.addstock(stock, qty, getStockPrice(stock))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    client = TradingClient(config.API_KEY, config.SECRET_KEY, paper=True)
    portfolio = StockPortfolio("Test")
    portfolio.printstocks()
    buyStocks(client, "AMZN", 1, OrderSide.BUY, TimeInForce.DAY, portfolio)

    # portfolio.printstocks()
    # order = client.submit_order(order_data=order_details)
