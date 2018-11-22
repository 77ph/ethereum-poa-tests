import datetime
import json
import web3
import sys
import time
import pprint
import sys
import os

from web3 import Web3, HTTPProvider, TestRPCProvider, shh
from web3.contract import ConciseContract
from web3.auto import w3
from web3.middleware import geth_poa_middleware

def wait_for_receipt(w3, tx_hash, poll_interval):
	while True:
		tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
		if tx_receipt:
			return tx_receipt
		time.sleep(poll_interval)

# print(sys.argv[1]) # prints var1
verbose = 1
contract_address = "0x84bf36fb797f93cd0e322b69c16bf99fc2e59459"

#my_provider = Web3.IPCProvider('/home/andrey/vcnet/geth.ipc')
my_provider = Web3.HTTPProvider('http://localhost:8502')
w3 = Web3(my_provider)
w3.middleware_stack.inject(geth_poa_middleware, layer=0)

if verbose:
	connected = w3.isConnected()
	node = w3.version.node
	print('Connected status {0} with node: "{1}!"'.format(connected, node))

with open('Counter.json') as f:
     ADDCHUNK_ABI = json.load(f)

dbAddress = Web3.toChecksumAddress(contract_address)
contract = w3.eth.contract(address=dbAddress, abi=ADDCHUNK_ABI)

if verbose:
	count = contract.functions.getCount().call()
	print('Contract Counter. count records: {}'.format(count))
 
print("Sending transaction \n")


ms = shh.Shh(w3)
pprint(ms)
print('version shh: ', ms.version)

with open("./vcnet2/keystore/UTC--2018-10-11T10-31-16.260152486Z--1d94baec6903bd722953d1111d3b03ea3fa99378") as keyfile:
	encrypted_key = keyfile.read()
	private_key = w3.eth.account.decrypt(encrypted_key, '123456')

id = ms.addPrivateKey(key=privatekey)
print('id ===>>>> ', id)
user_pubkey = ms.getPublicKey(id)
print('user_pubkey ===>>> ', user_pubkey)

topic = Web3.toHex(b'1111')
text = b'Hello world'
mes_send = ms.post(
    {
        'payload': Web3.toHex(text),
        'topic': topic,
    }
)
if mes_send:
	print('Message Send')
else:
	print('Message not send')

####
start = datetime.datetime.now()
count = 1

while True:
	tx_hash = contract.functions.incrementCounter().transact({'from': w3.eth.coinbase})
	current = datetime.datetime.now()
	elapsed = current - start
	# print(elapsed.seconds,":",elapsed.microseconds)
	if(elapsed.seconds > 1):		
		print("seconds = {0} transact count {1}".format(elapsed.seconds,count))
		count = contract.functions.getCount().call()
		print('Contract AddChunk. count records: {0}'.format(count))
		sys.exit()
	count = count + 1		 
	time.sleep(2.0/1000.0)

