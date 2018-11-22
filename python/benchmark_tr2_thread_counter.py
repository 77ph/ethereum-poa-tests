#!/usr/bin/env python3
"""
Advanced generator TX to vcnet2 using Contract Counter. Multithread. 
Call N:10000 function incrementCounter() via multi-threading queue with M:2-5 workers.

./benchmark_tr2_thread_counter.py
ABI = Counter.json
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

def many_transactions_threaded_Queue(contract, numTx, num_worker_threads):
	print ("send %d transactions, via multi-threading queue with %d workers:\n" % (numTx, num_worker_threads))

	q = Queue()
	def worker():
		while True:
			item = q.get()
			# print("contract from many_transactions_threaded_Queue  = {0} {1}".format(contract,type(contract)))
			contract_set_via_web3(contract)
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


def contract_set_via_web3(contract,gas=90000):
	# print("addchunk from contract_set_via_web3 = {0} {1}".format(addchunk,type(addchunk)))
	# print("contract from contract_set_via_web3 = {0} {1}".format(contract,type(contract)))
	tx = contract.functions.incrementCounter().transact({'from': w3.eth.coinbase, 'gas' : gas})
	# print ("[sent via web3]", end=" ")
	#tx = w3.toHex(tx)
	return tx



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
mycontract = w3.eth.contract(address=dbAddress, abi=ADDCHUNK_ABI)

if verbose:
	count = mycontract.functions.getCount().call()
	print('Contract Contract. count records: {}'.format(count))
 
print("Sending transaction \n")

####
start = datetime.datetime.now()
count = 1
numTs = 10000
workerTs = 5

while True:
	many_transactions_threaded_Queue(mycontract, numTs, workerTs)
	current = datetime.datetime.now()
	elapsed = current - start
	# print(elapsed.seconds,":",elapsed.microseconds)
	if(elapsed.seconds > 1):
		print("seconds = {0} microseconds {1} transact count {2}".format(elapsed.seconds,elapsed.microseconds,numTs))
		count = mycontract.functions.getCount().call()
		print('Contract Count. count records: {0}'.format(count))
		sys.exit()
	time.sleep(2.0/1000.0)

