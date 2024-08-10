f""" rom django.http import JsonResponse
from .blockchain import get_contract

def my_contract_view(request):
    contract = get_contract()
    try:
        # Llamar a una función del contrato
        result = contract.functions.myFunction().call()
        return JsonResponse({'result': result})
    except Exception as e:
        return JsonResponse({'error': str(e)}) """
