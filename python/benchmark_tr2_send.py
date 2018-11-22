#!/usr/bin/env python3
"""
Generator TX to vcnet2 without smart-contract. Single thread. 
Send a N wei from eth.coinbase to pre-defined eth-node (vcnet2) using RAW transaction.

./benchmark_tr2_send.py 0 ~/vcnet2/keystore/UTC--2018-10-11T10-31-16.260152486Z--1d94baec6903bd722953d1111d3b03ea3fa99378 123456
0 - start number for nonce
~/vcnet2/keystore/UTC--2018-10-11T10-31-16.260152486Z--1d94baec6903bd722953d1111d3b03ea3fa99378 - encrypted keystore
123456 - plaintext password
"""
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


def file2job(file_name):
	a,b,c = file_name.split("-")
	return (a,b)

# print(sys.argv[1]) # prints var1
verbose = 1
contract_address = "0x14f11783528da0e6a5aa273154c83446ef47ef57"
recipientAddress = "0xfcac2bff0e122322851dbaff6ea24f43dcd0e646"

#my_provider = Web3.IPCProvider('/home/andrey/vcnet/geth.ipc')
my_provider = Web3.HTTPProvider('http://localhost:8502')
w3 = Web3(my_provider)
w3.middleware_stack.inject(geth_poa_middleware, layer=0)

if verbose:
	connected = w3.isConnected()
	node = w3.version.node
	print('Connected status {0} with node: "{1}!"'.format(connected, node))

recipientAddress = Web3.toChecksumAddress(recipientAddress)

print("Sending transaction \n")

####
start = datetime.datetime.now()
count = 1

# "./vcnet2/keystore/UTC--2018-10-11T10-31-16.260152486Z--1d94baec6903bd722953d1111d3b03ea3fa99378"

instance=int(sys.argv[1])

with open(sys.argv[2]) as keyfile:
	encrypted_key = keyfile.read()
	private_key = w3.eth.account.decrypt(encrypted_key, sys.argv[3]) #password

money_to_frend=1
mynonce=w3.eth.getTransactionCount(w3.eth.coinbase)+instance

while True:
	#tx_hash = addchunk.functions.addChunkInfo(job_id, client_id, node_id, chunk_time, chunk_size, node_type).transact({'from': w3.eth.coinbase})
	#tx_hash = w3.eth.sendTransaction({from:eth.coinbase, 2f45731160c02f69cad1ff8ab9a48492dc3b2022, value: web3.toWei(11, "ether")})
	signed_txn = w3.eth.account.signTransaction(dict(nonce=mynonce,gasPrice = w3.eth.gasPrice, gas = 100000, to=recipientAddress,value=w3.toWei(money_to_frend,'ether')),private_key)
	tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
	# tx_hash = wait_for_receipt(w3,tx_hash,0.1)
	current = datetime.datetime.now()
	elapsed = current - start
	# print(elapsed.seconds,":",elapsed.microseconds)
	if(elapsed.seconds > 60):
		print("seconds = {0} transact count {1}".format(elapsed.seconds,count))
		total = money_to_frend*count
		print('Send to {0}. count tp: {1} , total send: {2}'.format(recipientAddress, count, total))
		sys.exit()
	count = count + 1
	mynonce = mynonce + 1		 
	time.sleep(2.0/1000.0)

