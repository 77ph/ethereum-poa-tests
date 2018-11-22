Tests of the ethereum POA Network
=================================


**Main objective** :

The purpose of the tests was to create a simple TPS measurement method (transactoins per second) of POA ethereum networks with different parameters and for different types of transactions.


**Networks and Parameters** :

2 types of networks were used for tests:
- vcnet5 - (5 sec block_period, 4700000 GasLimit)
- vcnet2 - (1 sec block_period, 23000000 GasLimit)

**Testing scheme**
![Testing scheme](https://github.com/77ph/ethereum-poa-tests/blob/master/docs/poa%20tests.png)

**Contracts**

To ensure a significant difference in the value of a single transaction, two contracts were created.

- Addchunk - an unindexed array of structs (cost per tx ~ 156к Gas)
- Counter - just simple counter (cost per tx ~ 27к Gas)

**Transactions generators**

- *benchmark_tr.py* Description: generator TX to vcnet using Contract AddChunk. Single thread. Call a functions.addChunkInfo with 20 ms delay in 600s. 
- *benchmark_tr2_thread.py* Description: Advanced generator TX to vcnet2 using Contract AddChunk. Multithread. Call N:10000 function.addChunkInfo() via multi-threading queue with M workers.
- *benchmark_tr2_counter.py* Description: generator TX to vcnet2 using Contract Counter. Single thread. Call a function incrementCounter() with 2 ms delay in 600s. 
- *benchmark_tr2_thread_counter.py* Description: Advanced generator TX to vcnet2 using Contract Counter. Multithread. Call N:10000 function incrementCounter() via multi-threading queue with M:2-5 workers.
- *benchmark_tr2_send.py* Description: generator TX to vcnet2 without smart-contract. Single thread. Send a N wei from eth.coinbase to pre-defined eth-node (vcnet2) using RAW transaction.

**Measurement tool**

- *txpool2.py* 2> log.file Description: Measurer state txpool in network (via w3 RPC) and counter mined, pending and queued transactions in poa network per time. Worked together with generator. log.file source for plot.


**Abstract calculations for TPS**

With accoradance to Ethereum Yellow book, theoretical limit  for TPS described as:

- tps = gaslimit / transaction_cost * block_period;

- the minimal cost of transaction in Ethereum is 21000 wei

Thus we can estimate the theoretical limits for our two networks and two contracts

- tps = 6 (vcnet5, addchunk)
- tps = 35 (vcnet5, counter)
- tps = 147 (vcnet2, addchunk)
- tps = 852 (vcnet2, counter)


**Report**

Full scope of results with more interested graphs is represented in [report](https://github.com/77ph/ethereum-poa-tests/blob/master/docs/General%20description%20of%20the%20%20POA%20ethereum%20tests.docx)



