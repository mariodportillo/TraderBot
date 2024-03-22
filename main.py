from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest
from datetime import date
import config

from yahoo_fin import stock_info

def getStockPrice(stock):

    return stock_info.get_live_price(stock)

class StockPortfolio:
    def __init__(self, nameOfPortfolio):
        self.nameOfPortfolio = nameOfPortfolio
        self.numOfStock = 0
        self.stockInfo = {}

    def addstock(self, stock_name,
                 purchase_date, num_of_shares, cost_per_share):
        self.stockInfo[stock_name] = {
            purchase_date: {num_of_shares: cost_per_share}
        }
        self.numOfStock += 1

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

def buyStocks(client, stock, qty, side, time_in_force, portfolio):
    order_details = MarketOrderRequest(
        symbol=stock,
        qty=qty,
        side=side,
        time_in_force=time_in_force
    )
    today = date.today()
    allPositions = client.get_all_positions()



    order = client.submit_order(order_data=order_details)


    portfolio.addstock(stock, today, qty, getStockPrice(stock))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    client = TradingClient(config.API_KEY, config.SECRET_KEY, paper=True)
    portfolio = StockPortfolio("Test")

    buyStocks(client, "AMZN", 10, OrderSide.BUY, TimeInForce.DAY, portfolio)

    portfolio.printstocks()
    # order = client.submit_order(order_data=order_details)



