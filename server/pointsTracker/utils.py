import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotAllowed,
)


class APIResponse(object):
    """
    Handles converting basic response data into a foramtted Http Response
    """

    def __init__(self, response=None):
        super(APIResponse, self).__init__()
        self.response = response or {}

    def respond(self, pretty=False):
        self.response.update({'success': True, 'code': 200})

        json_kwargs = {
            'cls': DjangoJSONEncoder
        }
        if pretty:
            json_kwargs.update({
                'sort_keys': True,
                'indent': 4,
                'separators': (',', ': '),
            })

        return HttpResponse(
            json.dumps(self.response, **json_kwargs),
            content_type="application/json"
        )

    def bad_request(self):
        self.response.update({'error': True, 'code': 400})
        return HttpResponseBadRequest(
            json.dumps(self.response), content_type="application/json"
        )

    def not_authorized(self):
        self.response.update({'error': True, 'code': 401})
        return HttpResponseForbidden(
            json.dumps(self.response), content_type="application/json"
        )

    @staticmethod
    def method_now_allowed(request_method):
        return HttpResponseNotAllowed(permitted_methods=request_method)


def get_request_data(request, method):
    """
    Handles retrieving relevant information from a request object
    """

    request_data = getattr(request, method, None)
    if not request_data and 'application/json' in request.content_type:
        request_data = json.loads(request.body)

    return request_data
