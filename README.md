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
- Counter - just simple counter (cost per tx ~ 23к Gas)
