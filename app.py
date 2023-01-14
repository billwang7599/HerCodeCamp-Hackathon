import requests
from time import sleep
 
API_KEY = {'X-API-Key': 'T8KJ8OOF'}
s = requests.session()
s.headers.update(API_KEY)
 
url = 'http://localhost:9999/v1/'
 
resp = s.get(url+'case')
 
resp.json()
 
 
case_info = resp.json()
tick = case_info['tick']
 
def get_tick(s):
    resp = s.get(url+'case')
    if resp.ok: # .ok means that the connection is established
        case = resp.json()
        return case['tick']
 
def security_info(s, ticker):
    payload = {'ticker': ticker}
    resp = s.get(url + 'securities', params=payload)
    if resp.ok:
        security_info = resp.json()
        return security_info[0]
 
# getting top of the book prices
 
def ticker_bid_ask(s, ticker):
    payload = {'ticker': ticker}
    resp = s.get(url + 'securities/book', params=payload)
    if resp.ok:
        book = resp.json()
        return book['bids'][0]['price'], book['asks'][0]['price']
 
def vwap(s, ticker):
    payload = {'ticker': ticker}
    resp = s.get(url + 'securities', params=payload)
    if resp.ok:
        book = resp.json()
        return book[0]['vwap']
 
def position(s):
    payload = {'ticker': 'CRZY_M'}
    resp = s.get(url +  'securities', params=payload)
    if resp.ok:
        return resp.json()[0]['position']
 
def buy(s, x, amount):
    if x == 'a':
        s.post(url + 'orders', params = {'ticker':'CRZY_A', 'type':'MARKET', 'quantity': amount, 'action': 'BUY'})
    elif x == 'm':
        s.post(url + 'orders', params = {'ticker': 'CRZY_M', 'type': 'MARKET', 'quantity': amount, 'action': 'BUY'})
    else:
        print("No ticker found")
   
def sell(s, x, amount):    
    if x == 'a':
        s.post(url + 'orders', params = {'ticker':'CRZY_A',
            'type':'MARKET', 'quantity': amount, 'action': 'SELL'})
    elif x == 'm':
        s.post(url + 'orders', params = {'ticker': 'CRZY_M',
            'type': 'MARKET', 'quantity': amount, 'action': 'SELL'})
    else:
        print("No ticker found")
 
 
# building a main function
 
def arb():
    tick = get_tick(s)
    while tick > 0 and tick < 301:
        m_bid, m_ask = ticker_bid_ask(s, 'CRZY_M')
        a_bid, a_ask = ticker_bid_ask(s, 'CRZY_A')
        """ a_vwap = vwap(s, 'CRZY_A')
        m_vwap = vwap(s, 'CRZY_M')
        pos = position(s) """
       
        x = 8000
        dev = 0.0
        if m_bid > a_ask + dev:
            buy(s, 'a', x)
            sell(s, 'm', x)
 
        if a_bid > m_ask + dev:
            buy(s, 'm', x)
            sell(s, 'a', x)
       
        # added after
        if m_bid > m_ask + dev:
            buy(s, 'm', x)
            sell(s, 'm', x)
 
        if a_bid > a_ask + dev:
            buy(s, 'a', x)
            sell(s, 'a', x)
       
        """ if tick < 10:
            if m_ask < a_ask:
                buy(s, 'm', 1)
            else:
                sell(s, 'a', 1)
  """
 
 
        """ x = 2000
        if pos < 22000 and pos > 0:
            if a_ask < (a_vwap - a_vwap*0.01):
                buy(s, 'a', x)
 
            if m_ask < (m_vwap - m_vwap*0.01):
                buy(s, 'm', x)
           
            if a_bid > (a_vwap*1.01):
                sell(s, 'a', x)
           
            if m_bid > (m_vwap*1.01):
                sell(s, 'm', x) """
       
 
 
 
 
        """ if (tick > 150 or pos >= 25000) and pos > 0:
            if m_bid > a_bid:
                sell(s, 'm', 400)
            else:
                sell(s, 'a', 400) """
 
        sleep((2.5 * 10**-3))
        tick = get_tick(s)
arb()
