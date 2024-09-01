from flask import Flask
from web3 import Web3

from app import app

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

if not web3.is_connected():
    print("Error: Not connected to Ganache")
else:
    print("Connected to Ganache")


web3.eth.default_account = web3.eth.accounts[0]

if __name__ == '__main__':
    app.run(debug=True, port=5000)
