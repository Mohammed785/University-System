from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.contrib import messages
from django.http.response import HttpResponseForbidden
from django.contrib.auth.models import AnonymousUser
from rest_framework import exceptions
from functools import wraps
#try it with userpasstest

def check_anonymous(func):
    @wraps(func)
    def wrapper(request,*args,**kwargs):
        if isinstance(request.user,AnonymousUser):
            raise exceptions.NotAuthenticated
        return func(request,*args,**kwargs)
    return wrapper

def check_login(func):
    @wraps(func)
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            messages.warning(request,'You Are Already Logged In')
            return redirect('home')
        else:
            return func(request,*args,**kwargs)
    return wrapper

def check_prof_previlage(func):
    @wraps(func)
    def wrapper(request,*args,**kwargs):
        if not request.user.is_prof:
            return HttpResponseForbidden
        else:
            return func(request,*args,**kwargs)
    return wrapper
