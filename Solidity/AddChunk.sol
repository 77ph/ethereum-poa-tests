pragma solidity ^0.4.24;

contract AddChunk {

 event Deposit(address from, uint value);


 function() payable {
   if (msg.value > 0)
     Deposit(msg.sender, msg.value);

 }

  
  struct 
   Chunk {
    uint job_id;
    address client_id;
    address node_id;
    uint chunk_time;
    uint chunk_size;
    bytes32 node_type;
  }
  
  
 
 
 //Chunk public chunk;

 Chunk [] public chunks;
 
 
 // Chunk info add to array event
 
 event AddChunkInfo(uint newJob_id, address newClient_id, address newNode_id, uint newChunk_time, uint newChunk_size, bytes32 newNode_type);
 
 
  
 function addChunkInfo(uint newJob_id, address newClient_id, address newNode_id, uint newChunk_time, uint newChunk_size, bytes32 newNode_type) {
 chunks.push(Chunk({job_id:newJob_id, client_id:newClient_id, node_id:newNode_id, chunk_time:newChunk_time, chunk_size:newChunk_size, node_type:newNode_type}));
 
 AddChunkInfo( newJob_id,  newClient_id,  newNode_id,  newChunk_time,   newChunk_size,  newNode_type);
 }
 
 
 
 function getCount()
    public
    constant
    returns(uint Count)
 {
    return chunks.length;
 }
 
 
     
 function getLastRec() constant returns(uint _job_id, address _client_id, address _node_id, uint _chunk_time, uint _chunk_size, bytes32 _node_type) {
   if(chunks.length < 1) throw;
  _job_id = chunks[chunks.length-1].job_id;
  _client_id = chunks[chunks.length-1].client_id;
  _node_id = chunks[chunks.length-1].node_id;
  _chunk_time = chunks[chunks.length-1].chunk_time;
  _chunk_size = chunks[chunks.length-1].chunk_size;
  _node_type = chunks[chunks.length-1].node_type;
 }

 function getRec(uint index) constant returns(uint _job_id, address _client_id, address _node_id, uint _chunk_time, uint _chunk_size, bytes32 _node_type) {
   if(chunks.length < 1 || index > chunks.length) throw;
           
        _job_id = chunks[index].job_id;
        _client_id = chunks[index].client_id;
        _node_id = chunks[index].node_id;
        _chunk_time = chunks[index].chunk_time;
        _chunk_size = chunks[index].chunk_size;
        _node_type = chunks[index].node_type;
        
 }

 function kill(address _to) {
    suicide(_to);
 }
}
