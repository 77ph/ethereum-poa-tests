import datetime
import json
import web3
import sys
import time
import pprint
import sys
import os

from web3 import Web3, HTTPProvider, TestRPCProvider
from web3.contract import ConciseContract
from web3.auto import w3
from web3.middleware import geth_poa_middleware

def wait_for_receipt(w3, tx_hash, poll_interval):
        while True:
                tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
                if tx_receipt:
                        return tx_receipt
                time.sleep(poll_interval)

def str2bytes32(str):
        len1 = len(str)
        zBytes = str
        if len1 > 32:
                zBytes32 = zBytes[:32]
        else:
                zBytes32 = zBytes.ljust(32, '0')
        xBytes32 = bytes(zBytes32, 'utf-8')
        return xBytes32


my_provider = Web3.HTTPProvider('http://localhost:8502')
# my_provider = Web3.IPCProvider('/home/andrey/vcnet/geth.ipc')
w3 = Web3(my_provider)
w3.middleware_stack.inject(geth_poa_middleware, layer=0)
contract_address = "0x14f11783528da0e6a5aa273154c83446ef47ef57"

with open('AddChunk.json') as f:
     ADDCHUNK_ABI = json.load(f)

verbose = 1

if verbose:
        connected = w3.isConnected()
        node = w3.version.node
        print('Connected status {0} with node: "{1}!"'.format(connected, node))

dbAddress = Web3.toChecksumAddress(contract_address)
addchunk = w3.eth.contract(address=dbAddress, abi=ADDCHUNK_ABI)

if verbose:
        count = addchunk.functions.getCount().call()
        print('Contract AddChunk. count records: {}'.format(count))

start = datetime.datetime.now()

while True:
        receipt = w3.txpool.status
        print("txpool status")
        pprint.pprint(dict(receipt))
        p1 = dict(receipt)
        pending = p1["pending"]
        pending = int(pending, 16)
        print(pending)
        queued = p1["queued"]
        queued = int(queued, 16)
        current = datetime.datetime.now()
        elapsed = current - start
        count = addchunk.functions.getCount().call()
        print("{0},{1},{2},{3}".format(elapsed.seconds,pending,queued,count), file=sys.stderr)
        print("Time after start [secs] : {0} [microseconds] {1}".format(elapsed.seconds,elapsed.microseconds))
        time.sleep (10.0)

