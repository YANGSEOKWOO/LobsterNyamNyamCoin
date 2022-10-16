import time
import pyupbit
import datetime

access = "0YjQquXVtx4VlRLLNRc1tbKR9CT6fJDgMzstwdb4"
secret = "eN4jZxqxKBqwpkiTbxAgGFfvEtGYq0lYirZOjnxU"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

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

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-SOL")
        end_time = start_time + datetime.timedelta(days=1)
        wasSold = 0

        target_price = get_target_price("KRW-SOL", 0.5)
        current_price = get_current_price("KRW-SOL")
        #사는 타이밍: 변동성 돌파 전력이랑 똑같음
        if target_price < current_price and wasSold == 0:
            krw = get_balance("KRW")
            if krw > 5000:
                upbit.buy_market_order("KRW-SOL", krw*0.9995)
                wasSold = 0
        # 파는 타이밍: 5프로 손해 또는 시간 끝
        if current_price <= target_price * 0.95:
            upbit.sell_market_order("KRW-SOL", btc * 0.9995)
            wasSold = 1
        if now > end_time - datetime.timedelta(seconds=10) and wasSold != 1:
            btc = get_balance("SOL")
            if btc > 0.00008:
                upbit.sell_market_order("KRW-BTC", btc*0.9995)
                time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
