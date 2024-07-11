import json
from django.shortcuts import render, redirect
from web3 import Web3
from .models import InventoryItem

infura_url = 'https://mainnet.infura.io/v3/bd836856f4e94fa3801743a6419f5f80'
web3 = Web3(Web3.HTTPProvider(infura_url))
contract_address = '0xd9145CCE52D386f254917e481eB44e9943F39138'
contract_abi = 'your_contract_abi'

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def add_item(request):
    if request.method == 'POST':
        name = request.POST['name']
        quantity = int(request.POST['quantity'])
        tx_hash = contract.functions.addItem(name, quantity).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        return redirect('inventory')
    return render(request, 'add_item.html')

def inventory(request):
    items = []
    item_count = contract.functions.itemCount().call()
    for item_id in range(1, item_count + 1):
        item = contract.functions.getItem(item_id).call()
        items.append({'id': item[0], 'name': item[1], 'quantity': item[2]})
    return render(request, 'inventory.html', {'items': items})
