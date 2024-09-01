from flask import request, jsonify,render_template
from app import app
from run import web3

contract_abi = [
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "name": "cvElements",
      "outputs": [
        {
          "internalType": "string",
          "name": "element",
          "type": "string"
        },
        {
          "internalType": "bool",
          "name": "verified",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "_name",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_element",
          "type": "string"
        }
      ],
      "name": "submitCVElement",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "_name",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_element",
          "type": "string"
        },
        {
          "internalType": "bool",
          "name": "_verified",
          "type": "bool"
        }
      ],
      "name": "verifyCVElement",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "_name",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_element",
          "type": "string"
        }
      ],
      "name": "checkVerificationStatus",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    }
  ]  # Add your contract's ABI here
contract_address = "0x41D512cFeF22624E827Ee1A286A48967A3414f51"

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_cv', methods=['GET', 'POST'])
def submit_cv():
    if request.method == 'POST':
        data = request.json
        name = data.get('name')
        element = data.get('element')
        tx_hash = contract.functions.submitCVElement(name, element).transact()
        web3.eth.wait_for_transaction_receipt(tx_hash)
        return jsonify({'message': 'CV element submitted for verification', 'tx_hash': tx_hash.hex()}), 200
    return render_template('submit_cv.html')

@app.route('/verify_cv', methods=['GET', 'POST'])
def verify_cv():
    if request.method == 'POST':
        data = request.json
        name = data.get('name')
        element = data.get('element')
        verified = data.get('verified')
        tx_hash = contract.functions.verifyCVElement(name, element, verified).transact()
        web3.eth.wait_for_transaction_receipt(tx_hash)
        return jsonify({'message': 'CV element verification status updated', 'tx_hash': tx_hash.hex()}), 200
    return render_template('verify_cv.html')

@app.route('/check_status', methods=['GET'])
def check_status():
    name = request.args.get('name')
    element = request.args.get('element')
    
    # Ensure that both 'name' and 'element' are provided
    if not name or not element:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    try:
        # Call the smart contract function with the correct types
        status = contract.functions.checkVerificationStatus(name, element).call()
        return jsonify({'name': name, 'element': element, 'status': status}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

