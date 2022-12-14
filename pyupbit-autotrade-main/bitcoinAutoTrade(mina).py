import time
import pyupbit
import datetime
import pybithumb

access = "v6JlrnjNHQnxPZsmt7iqlhLsITaB1g4ywSAYpOVg"
secret = "fau8HNUewWHKXDiFDSTPdiSf1GlOdUi0CVunT8Sn"

#def get_target_price(ticker, k):
#   """변동성 돌파 전략으로 매수 목표가 조회"""
#df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
#    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
#    return target_price



def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0


def get_yesterday_ma3(ticker):
    """(3일)전일 이동평균"""
    df = pybithumb.get_ohlcv(ticker)
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    close = df['close']
    ma = close.rolling(3).mean()
    return ma[-2]



def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]


target_price = get_yesterday_ma3("KRW-SOL") #"전일이동평균 = 목표가"




# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-SOL")
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_yesterday_ma3("KRW-SOL")
            current_price = get_current_price("KRW-SOL")
           
            if target_price < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-SOL", krw*0.9995)
                    
        else:
            sol = get_balance("SOL")
            if sol > 0.00008:
                upbit.sell_market_order("KRW-SOL", sol*0.9995)
        
        all = pybithumb.get_current_price("SOL") 
        if all is None: 	
            break 
        current_price = pybithumb.get_current_price(target_price)
        if current_price is None: 	
            break

    except Exception as e:
        print(e)
        time.sleep(1)
