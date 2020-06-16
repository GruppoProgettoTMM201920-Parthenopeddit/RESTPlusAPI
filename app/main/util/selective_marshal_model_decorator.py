from functools import wraps

from flask_restplus import marshal


def selective_marshal_with(models):
    """
    Selective response marshalling. Doesn't update apidoc.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            object, code = func(*args, **kwargs)

            selected_model = None
            for candidate in models:
                if candidate['code'] == code:
                    selected_model = candidate['model']
                    break
            return marshal(object, selected_model), code
        return wrapper
    return decorator