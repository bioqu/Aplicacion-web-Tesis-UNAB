""" # blockchain.py
from web3 import Web3
from .config import GANACHE_URL, CONTRACT_ADDRESS, CONTRACT_ABI

# Conectar a Ganache
web3 = Web3(Web3.HTTPProvider(GANACHE_URL))

# Verificar conexión
if not web3.is_connected():
    raise Exception("No se pudo conectar a Ganache")

# Obtener el contrato
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

try:
    result = contract.functions.myFunction().call()
    print("Resultado de myFunction:", result)
except Exception as e:
    print(f"Error al llamar a la función del contrato: {e}")

def get_contract():
    return contract
 """