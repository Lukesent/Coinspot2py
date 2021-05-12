import requests
import time
from itertools import count
import hmac
import hashlib

header={
    '''Place your generated coinbase API key'''
    "key": "",
    "sign": ""
    }
secret_key = "" # Calls require HMAC-SHA512, this will be your security key. Ideally this should be 512bits in length. 
public_endpoint = "https://www.coinspot.com.au/pubapi/v2"
endpoint = "https://www.coinspot.com.au/api/v2"
quick_buy = "/quote/buy/now"
quick_sell = "/quote/sell/now"
quick_price = "/latest"
payload = {"cointype": "DOGE", "amount": "100", "amounttype": 'aud'}
payload_pc = {"cointype": "DOGE"}

NONCE_COUNTER = count(int(time.time() * 1000))

def status_check():
    # check stats
    # check root
    # check requests
    request = requests.Request('GET', endpoint, data=payload_pc, headers=header)
    prepare = request.prepare()
    prepare.headers['sign'] = hmac.new(secret_key, prepare.body, digestmod=hashlib.sha512)
    with requests.Session() as session:
        response = session.send(prepare)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: {response.status_code}"


def price():
    request = requests.Request('GET', endpoint+quick_price, data=payload_pc, headers=header)
    prepare = request.prepare()

    with requests.Session() as session:
        response = session.send(prepare)
        if response.status_code == 200:
            return response.json()["prices"]["DOGE"]["last"]
        else:
            return f"Error: status code: {response.status_code}\nmessage: {response.json()['message']}" 


def buy():
    request = requests.Request('GET', endpoint+quick_buy, data=payload, headers=header)
    prepare = request.prepare()
    payload['nonce'] = next(NONCE_COUNTER)
    sig = hmac.new(secret_key, prepare.body, digestmod=hashlib.sha512)
    prepare.headers['sign'] = sig.hexdigest()
    with requests.Session() as session:
        response = session.send(prepare)
        if response.status_code == 200 and response.json()["status"] == "ok":
            return 0
        else: 
            return f"Error: {response.status_code}"


def sell():
    request = requests.Request('GET', endpoint+quick_sell, data=payload, headers=header)
    prepare = request.prepare()
    payload['nonce'] = next(NONCE_COUNTER)
    sig = hmac.new(secret_key, prepare.body, digestmod=hashlib.sha512)
    prepare.headers['sign'] = sig.hexdigest()
    with requests.Session() as session:
        response = session.send(prepare)
        if response.status_code == 200 and response.json()["status"] == "ok":
            return 0
        else: 
            return f"Error: {response.status_code}"


def trade():
    #while not key loop
    
    pass
      

if __name__=='__main__':
    print(f"Running. {status_check}")
    print("Force buy, force sell, panic stop")
    trade()
    pass
