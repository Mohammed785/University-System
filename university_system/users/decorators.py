from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from rest_framework import exceptions
from functools import wraps


def check_anonymous(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser):
            raise exceptions.NotAuthenticated
        return func(request, *args, **kwargs)

    return wrapper


def check_login(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "You Are Already Logged In")
            return redirect("home")
        else:
            return func(request, *args, **kwargs)

    return wrapper


def check_prof_privilege(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_prof:
            raise exceptions.PermissionDenied
        else:
            return func(request, *args, **kwargs)

    return wrapper


def try_expect(default_value, *errors):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            try:
                return func(request, *args, **kwargs)
            except errors:
                print(f"[ERROR] {repr(errors)}")
                raise default_value

        return wrapper

    return decorator
