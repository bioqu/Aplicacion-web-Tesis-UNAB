from web3 import Web3
from .config import INFURA_URL

web3 = Web3(Web3.HTTPProvider(INFURA_URL))

def check_connection():
    return web3.isConnected()
