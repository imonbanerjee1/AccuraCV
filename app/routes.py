from flask import request, jsonify,render_template
from app import app
from run import web3
from werkzeug.utils import secure_filename
import fitz
import os

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


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf'}

def process_pdf(filepath):
    doc = fitz.open(filepath)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return extract_cv_elements(text)

def extract_cv_elements(text):
    lines = text.split('\n')
    elements = {
        "personal_info": lines[0] if len(lines) > 0 else "",
        "education": lines[1] if len(lines) > 1 else "",
        "experience": lines[2] if len(lines) > 2 else "",
        "skills": lines[3] if len(lines) > 3 else ""
    }
    return elements

@app.route('/upload_cv', methods=['GET', 'POST'])
def upload_cv():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            cv_elements = process_pdf(filepath)
            
            return render_template('cv_elements.html', elements=cv_elements)
    return render_template('upload_cv.html')


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
            status = contract.functions.checkVerificationStatus(name, element).call()
            if status is None:
                message = "Invalid item"
            else:
                message = f"Verification Status for {element} under the name {name} is {status}."
            print(message)
            return render_template('check_status.html', status=status, message=message, name=name, element=element)
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    return render_template('check_status.html', status=None, message=None)
