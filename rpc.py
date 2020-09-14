import time, requests, json, re

# Don't forget to change this value if necessary
LIQUID_REG_1 = "http://elements:password1@127.0.0.1:18888"
LIQUID_REG_2 = "http://elements:password1@127.0.0.1:18885"

BITCOIN_REG = "http://bitcoin:password1@127.0.0.1:18444" # Bitcoin shouldn't work anyway
ELEMENTS_REG = LIQUID_REG_1
LIQUID = "http://elements:<password>=@127.0.0.1:7041" # Add the relevant password

# Obviously change that to the real path
CONF1 = "/home/sosthene/liquid/data/liquid1/elements.conf"
CONF2 = "/home/sosthene/liquid/data/liquid2/elements.conf"

class RPCHost:
    def __init__(self, chain):
        self._session = requests.Session()
        '''
        if re.match(r'.*\.onion/*.*', url):
            self._session.proxies = {}
            self._session.proxies['http'] = 'socks5h://localhost:9050'
            self._session.proxies['https'] = 'socks5h://localhost:9050'
        '''
        self._headers = {'content-type': 'application/json'}
        if chain == "bitcoin-regtest":
            self._url = BITCOIN_REG
            self._chain = chain
        elif chain == "elements-regtest":
            self._url = ELEMENTS_REG
            self._chain = chain
        elif chain == "liquid":
            self._url = LIQUID
            self._chain = chain
        else:
            raise ValueError("wrong chain value")

    def call(self, rpcMethod, *params):
        payload = json.dumps({"method": rpcMethod, "params": list(params), "jsonrpc": "2.0"})
        print(payload)
        tries = 5
        hadConnectionFailures = False
        while True:
            try:
                response = self._session.post(self._url, headers=self._headers, data=payload)
            except requests.exceptions.ConnectionError:
                tries -= 1
                if tries == 0:
                    raise Exception('Failed to connect for remote procedure call.')
                hadFailedConnections = True
                time.sleep(10)
            else:
                if hadConnectionFailures:
                    print('Connected for remote procedure call after retry.')
                break
        if not response.status_code in (200, 500):
            raise Exception('RPC connection failure: ' + str(response.status_code) + ' ' + response.reason)
        responseJSON = response.json()
        if 'error' in responseJSON and responseJSON['error'] != None:
            raise Exception('Error in RPC call: ' + str(responseJSON['error']))
        return responseJSON['result']
