from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("accounts:dashboard")
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_user(allowed_role=[]):
    def decorators(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_role:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("This is not a userpage")
        return wrapper_func
    return decorators


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == "admin":
            return view_func(request, *args, **kwargs)
        if group == "customer":
            return redirect("accounts:user-page")

    return wrapper_func