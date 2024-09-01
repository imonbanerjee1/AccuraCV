// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract CVVerification {
    struct CVElement {
        string element;
        bool verified;
    }

    mapping(string => mapping(string => CVElement)) public cvElements;

    function submitCVElement(string memory _name, string memory _element) public {
        cvElements[_name][_element] = CVElement(_element, false);
    }

    function verifyCVElement(string memory _name, string memory _element, bool _verified) public {
        cvElements[_name][_element].verified = _verified;
    }

    function checkVerificationStatus(string memory _name, string memory _element) public view returns (bool) {
        return cvElements[_name][_element].verified;
    }
}
