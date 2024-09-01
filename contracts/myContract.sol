// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract MyContract {
  string public message = "Hello, Blockchain!";
  
  function setMessage(string memory _message) public {
    message = _message;
  }
}
