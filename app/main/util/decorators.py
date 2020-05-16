from functools import wraps

from flask_restplus import marshal_with


# TODO implement wrapper for marshal with
def wrapped_marshal_with(fields, envelope=None):
    def wrapper(f):
        print("Do something with fields and envelope")

        @wraps(f)
        def inner(*args, **kwargs):
            rmw = marshal_with(fields, envelope)
            return rmw(f)(*args, **kwargs)
        return inner
    return wrapper
