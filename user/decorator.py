from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('user:home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:

                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'hocsinh':
            messages.success(request, 'Bạn không có quyền truy cập')
            return redirect('user:home')

        if group == 'admin':
            return view_func(request, *args, **kwargs)

    return wrapper_function

def hocsinh_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name


        if group == 'admin':
            return redirect('user:home')

        if group == 'hocsinh':
            return view_func(request, *args, **kwargs)

    return wrapper_function