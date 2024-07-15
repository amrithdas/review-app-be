from drf_yasg.utils import swagger_auto_schema
from functools import wraps

def custom_auto_schema(**kwargs):
    """
    Custom decorator to apply swagger_auto_schema globally.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(*args, **kwargs):
            return swagger_auto_schema(**kwargs)(view_func)(*args, **kwargs)
        return _wrapped_view
    return decorator