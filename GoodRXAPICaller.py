import hmac
import hashlib
import base64
import json
import urllib2

class GoodRXAPICaller(object):
    _API_KEY = 'f46cd9446f'
    _SECRET_KEY = 'c9lFASsZU6MEu1ilwq+/Kg=='
    _API_URL = 'https://api.goodrx.com/drug-search'

    def get_candidates(self, drugName):
        signature = self._form_signature(drugName)
        req = urllib2.Request('{}?query={}&api_key={}&sig={}'.format(self._API_URL, drugName, self._API_KEY, signature))
        resp = urllib2.urlopen(req).read()
        return self._parse_response(resp)

    def _parse_response(self, resp):
        jsonResp = json.loads(resp)
        if jsonResp['success']:
            return jsonResp['data']['candidates']
        return None

    def _form_signature(self, drugName):
        query_string = 'query={}&api_key={}'.format(drugName, self._API_KEY)
        signature = hmac.new(self._SECRET_KEY, msg=query_string, digestmod=hashlib.sha256).digest()
        signature = base64.b64encode(signature, "__")
        return signature
