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
        name = request.form['name']
        element = request.form['element']
        tx_hash = contract.functions.submitCVElement(name, element).transact()
        web3.eth.wait_for_transaction_receipt(tx_hash)
        return render_template('submit_cv.html', tx_hash=tx_hash.hex())
    return render_template('submit_cv.html')

@app.route('/verify_cv', methods=['GET', 'POST'])
def verify_cv():
    if request.method == 'POST':
        name = request.form['name']
        element = request.form['element']
        verified = request.form['verified'] == 'true'
        tx_hash = contract.functions.verifyCVElement(name, element, verified).transact()
        web3.eth.wait_for_transaction_receipt(tx_hash)
        return render_template('verify_cv.html', tx_hash=tx_hash.hex())
    return render_template('verify_cv.html')

@app.route('/check_status', methods=['GET', 'POST'])
def check_status():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        element = request.form.get('element')
        
        try:
            # Call the contract function to check the status
            status = contract.functions.checkVerificationStatus(name, element).call()
            
            # Handle the case where the CV element does not exist
            if status is None or status == False:
                message = "Invalid item"
            else:
                message = f"Verification Status for {element} under the name {name} is {status}."
            print(message)
            return render_template('check_status.html', status=status, message=message, name=name, element=element)
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    return render_template('check_status.html', status=None, message=None)
