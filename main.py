import investpy

class StockPortfolio:
    def __init__(self, nameOfPortfolio):
        self.nameOfPortfolio = nameOfPortfolio
        self.numOfStock = 0
        self.stockInfo = {}

    def addStock(self, stock_name,
                 purchase_date, num_of_shares, cost_per_share):
        self.stockInfo[stock_name] = {
            purchase_date: {num_of_shares: cost_per_share}
        }
    def printStocks(self):
        print(self.stockInfo)

    def deleteStock(self, deleted_stock):
        if deleted_stock in self.stockInfo:
            val = input("Type YES if you want to delete stock")

            if val == "YES":
                del self.stockInfo[deleted_stock]

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test = StockPortfolio("My First Test")
    test.addStock("DIS", "1/22/23", 30, 24.50)
    test.printStocks()
    test.deleteStock("DIS")
    test.printStocks()


