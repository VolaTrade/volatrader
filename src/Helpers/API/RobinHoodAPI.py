import robin_stocks as r


class RobinHood:
    def __init__(self):
        self.portfolio = {}
        self.session = r 

    def login(self, username: str, password: str):
        self.session.login(username=username, password=password)
        self.updatePortfolio()

    def updatePortfolio(self):
        for val in self.session.get_crypto_positions():
            if int(val['quantity'][0:1]) != 0: 
                print(val)
                self.portfolio[val['currency']['code']] = float(val['quantity'])

    def getPortfolio(self):
        return self.portfolio

    def logout(self):
        r.logout()
    
    def getPriceForAsset(self, symbol: str):
        return float(r.get_crypto_quote(symbol)['mark_price'])

    def sellAsset(self, symbol: str):
        r.order_sell_crypto_by_quantity(symbol, quantity=self.portfolio[symbol])
    
