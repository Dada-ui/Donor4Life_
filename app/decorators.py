from django.core.exceptions import PermissionDenied


def user_is_donor(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.role == 'donor':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def user_is_recipient(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.role == 'recipient':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap