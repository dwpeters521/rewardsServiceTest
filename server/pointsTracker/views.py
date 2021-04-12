from django.views.decorators.csrf import csrf_exempt

from .decorators import require_auth, validate_http_method
from .exceptions import NotEnoughBalanceException, InvalidInputException
from .models import (
    PayerBalance,
    Transaction,
)
from .utils import APIResponse, get_request_data


@csrf_exempt
@require_auth
@validate_http_method(method='POST')
def add_transaction(request):
    request_data = get_request_data(request, 'POST')

    try:
        Transaction.create(request_data)

    except NotEnoughBalanceException as error:
        error_message = error.args[0]
        return APIResponse({
            'errors': {
                'points': [error_message]
            }
        }).bad_request()

    except InvalidInputException as error:
        error_messages = error.args[0]
        return APIResponse(
            {'errors': error_messages}
        ).bad_request()

    return APIResponse().respond()


@csrf_exempt
@require_auth
@validate_http_method(method='POST')
def spend_points(request):
    request_data = get_request_data(request, 'POST')

    try:
        payers_and_points = Transaction.spend_points(request_data=request_data)

    except NotEnoughBalanceException as error:
        error_message = error.args[0]
        return APIResponse({
            'errors': {
                'points': [error_message]
            }
        }).bad_request()

    except InvalidInputException as error:
        error_messages = error.args[0]
        return APIResponse(
            {'errors': error_messages}
        ).bad_request()

    serialized_results = Transaction.serialize(payers_and_points)

    return APIResponse({'results': serialized_results}).respond()


@require_auth
@validate_http_method(method='GET')
def get_balance(request):
    request_data = get_request_data(request, 'GET')
    payer = request_data.get('payer')

    balance = PayerBalance.objects.get_balance_ordered_by_payer(payer)
    serialized_balance = PayerBalance.serialize(balance)

    return APIResponse({'results': serialized_balance}).respond()
