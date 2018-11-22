#!/usr/bin/env python3
"""
Advanced generator TX to vcnet2 using Contract AddChunk. Multithread. 
Call N:10000 function.addChunkInfo() via multi-threading queue with M workers.
./benchmark_tr2_thread.py
ABI = AddChunk.json
"""

import datetime
import json
import web3
import sys
import time
import pprint
import sys
import os

from threading import Thread
from queue import Queue


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



def many_transactions_threaded_Queue(contract, numTx, job_id, client_id, node_id, chunk_time, chunk_size, node_type, num_worker_threads):
	print ("send %d transactions, via multi-threading queue with %d workers:\n" % (numTx, num_worker_threads))

	q = Queue()
	def worker():
		while True:
			item = q.get()
			# print("contract from many_transactions_threaded_Queue  = {0} {1}".format(contract,type(contract)))
			contract_set_via_web3(contract, job_id, client_id, node_id, chunk_time, chunk_size, node_type)
			# print (".", end=""); sys.stdout.flush()
			q.task_done()

	for i in range(num_worker_threads):
		t = Thread(target=worker)
		t.daemon = True
		t.start()
	print (".", end=""); sys.stdout.flush()
	print ("%d worker threads created." % num_worker_threads)

	for i in range(numTx):
		q.put(i)
		print (".", end=""); sys.stdout.flush()

	print ("%d items queued." % numTx)

	q.join()
	print ("\nall items - done.")


def contract_set_via_web3(contract, job_id, client_id, node_id, chunk_time, chunk_size, node_type):
	# print("addchunk from contract_set_via_web3 = {0} {1}".format(addchunk,type(addchunk)))
	# print("contract from contract_set_via_web3 = {0} {1}".format(contract,type(contract)))        
	tx = contract.functions.addChunkInfo(job_id, client_id, node_id, chunk_time, chunk_size, node_type).transact({'from': w3.eth.coinbase})
	# print ("[sent via web3]", end=" ")
	#tx = w3.toHex(tx)
	return tx



# print(sys.argv[1]) # prints var1
verbose = 1
contract_address = "0x14f11783528da0e6a5aa273154c83446ef47ef57"
node_type = 'distributor'
client_id = "0x14f11783528da0e6a5aa273154c83446ef47ef57"
job_id = 100
chunk_size = 100000

#my_provider = Web3.IPCProvider('/home/andrey/vcnet/geth.ipc')
my_provider = Web3.HTTPProvider('http://localhost:8502')
w3 = Web3(my_provider)
w3.middleware_stack.inject(geth_poa_middleware, layer=0)

if verbose:
	connected = w3.isConnected()
	node = w3.version.node
	print('Connected status {0} with node: "{1}!"'.format(connected, node))

with open('AddChunk.json') as f:
     ADDCHUNK_ABI = json.load(f)

dbAddress = Web3.toChecksumAddress(contract_address)
addchunk = w3.eth.contract(address=dbAddress, abi=ADDCHUNK_ABI)

print("addchunk = {0}".format(type(addchunk)))

if verbose:
	count = addchunk.functions.getCount().call()
	print('Contract AddChunk. count records: {}'.format(count))
 
# client_id = "fcac2bff0e122322851dbaff6ea24f43dcd0e646"
node_id = w3.eth.coinbase

client_id = Web3.toChecksumAddress(client_id)
node_id = Web3.toChecksumAddress(node_id)

# https://ethereum.stackexchange.com/questions/30683/how-send-bytes32-in-web3-py
node_type = str2bytes32(node_type)
chunk_time = int(time.time())

print("Sending transaction \n")

####
start = datetime.datetime.now()
count = 1

while True:
	many_transactions_threaded_Queue(addchunk, 10000, job_id, client_id, node_id, chunk_time, chunk_size, node_type, 5) # TX = 10000, workers = 5
	current = datetime.datetime.now()
	elapsed = current - start
	# print(elapsed.seconds,":",elapsed.microseconds)
	if(elapsed.seconds > 60):
		print("seconds = {0} microseconds {1} transact count {2}".format(elapsed.seconds,elapsed.microseconds,10000))
		count = addchunk.functions.getCount().call()
		print('Contract AddChunk. count records: {0}'.format(count))
		sys.exit()
	time.sleep(2.0/1000.0)

