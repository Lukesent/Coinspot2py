import requests
import json
from time import time
import hmac
import hashlib
from itertools import count


class coinspot:
    '''Coinspot API v2 Python Wrapper
    Implemented by: https://github.com/Lukesent
    Documentation: https://www.coinspot.com.au/v2/api 
    '''
    NONCE_COUNTER = count(int(time() * 1000))
    _api_key = ""
    _api_secret = b""
    _endpoint = "https://www.coinspot.com.au/api/v2"


    def __init__(self, api_key, api_secret):
        ''''''
        self._api_key = api_key 
        self._api_secret = api_secret
        #self.keyset()


    def keyset(self):
        ''''''
        with open('key.txt','r') as f:
            try:
                pass
                #self._api_key = f.read(32)
                #self._api_secret = bytes(f.read(80), 'utf-8')
            except IOError as err:
                print(f"Error reading key file {err}")

            
    def sign_request(self, data):
        '''Signing request'''
        return hmac.new(self._api_secret, data.encode('utf-8'), digestmod=hashlib.sha512).hexdigest()
    

    def request(self, path, postdata):
        '''Sending all requests to Coinspot'''
        postdata['nonce'] = next(self.NONCE_COUNTER)
        
        params = json.dumps(postdata, separators=(',', ':'))
        signedMessage = self.sign_request(params)

        headers = {
        'Content-type' : 'application/json',
        'key' : self._api_key,
        'sign' : signedMessage
        }

        request = requests.post(self._endpoint+path, headers=headers, data=postdata)
        return request


    def buy(self, coin, amount_AUD):
        '''Buy selected coin in AUD'''
        path = '/my/buy/now'
        try:
            self.request(path, {'cointype': coin, 'amounttype': 'aud', 'amount': amount_AUD})
        except requests.models.HTTPError as err:
            print(f"Error with request {err}")


    def sell(self, coin, amount_AUD):
        '''Sell selected coin in AUD'''
        path = '/my/sell/now'
        try:
            self.request(path, {'cointype': coin, 'amounttype': 'aud', 'amount': amount_AUD})
        except requests.models.HTTPError as err:
            print(f"Error with request {err}")
            
        
