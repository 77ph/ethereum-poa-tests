pragma solidity ^0.4.24;

contract Counter {
    int private count = 0;

    function incrementCounter() public {
        count += 1;
    }
    
    function derementCounter() public {
    require(count!=0);
        count -= 1;
    }

    function clearCounter() public {
        count  = 0;
    }

    function getCount() public constant returns (int) {
        return count;    
    }
}
