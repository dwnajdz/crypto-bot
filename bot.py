import time
import yfinance as yf
from datetime import datetime

stock_symbol = str(input('Please type stock symbol (CRYPTO-CURRENCY, ADA-USD, BTC-USD): '))
budget = int(input('Please type budget ($USD): ')) 

class Wallet():
    def __init__(self, user_budget):
        self.active_money = user_budget

    active_money = 0
    earnings = 0
    portfolio = {}

    def buy(self, price):
        if price > self.active_money:
            return

        key = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # buy only 50% of amount
        amount = int(self.active_money//price)//2
        buying = price*amount

        if buying > self.active_money:
            print(f'Insufficent funds... Wants:{buying} Balance: {self.active_money}')
            return

        self.active_money -= buying
        # portfolio[current_date] = [stock_value, buying_price, amount]
        # portfolio[12-12-2008 17:12:30] = [253.1, '0.38', 1048]
        self.portfolio[key] = [price, amount]
        print(f'Buyed: {buying}, Active money: {self.active_money}')
        print(f'Your portfolio: {self.portfolio}')

    def check_for_sell(self, price):
        print('Checking for sell moment..')
        # doing copy of portfolio here because otherwise 
        # it will return error if we try to pop key inside a loop
        for key, value in self.portfolio.copy().items():
            print(f'Trying to sell: {key}')
            buying_price = value[0]
            amount = value[1] 
            #buying_price+0.5 because we want actually to earn some money
            if buying_price+0.5 < price:
                self.active_money += price*amount
                self.earnings += (self.active_money)-(buying_price*amount)
                print(f'Selled_key: {key}, Price: {buying_price*amount}, Current: {self.active_money}, Selled amount: {amount}')
                self.portfolio.pop(key)
                
        return

def realtime() -> any:
    data = yf.download(stock_symbol, period='1d', interval='1m', threads=True, progress=False)
    return data

def mean() -> any:
    data = yf.download(stock_symbol, period='1mo', interval='1d', threads=True, progress=False)
    return data['Close'].mean()

month_mean = mean()
print(f'Last month mean price: {month_mean}')
myWallet = Wallet(budget)

while True:
    current_price = realtime()['Close'][-1]
    print(f'Current price: {current_price}')
    if current_price < month_mean:
        myWallet.buy(current_price)
    else:
        print(f'mean price = {month_mean}, possible_earning: {month_mean-current_price}')
    time.sleep(10.0)
    myWallet.check_for_sell(current_price)
    time.sleep(10.0)

print('Ending...')
