from .auth import is_authenticated
from .utils import APIResponse


def require_auth(f):
    """
    Decorator to handle requests to endpoints by first verifying the request is
    authenticated
    """

    def wrapper(request, *args, **kwargs):
        if is_authenticated(request):
            return f(request, *args, **kwargs)
        else:
            return APIResponse().not_authorized()

    wrapper.__doc__ = f.__doc__
    wrapper.__name__ = f.__name__
    return wrapper


def validate_http_method(**kwargs):
    def inner(func):
        def wrapper(request):
            request_method = kwargs['method']
            if request.method == request_method:
                return func(request)
            else:
                return APIResponse.method_now_allowed(request_method)

        return wrapper

    return inner
