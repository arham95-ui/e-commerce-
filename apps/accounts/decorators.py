from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def user_not_authenticated(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('shop:home')
        return view_func(request, *args, **kwargs)
    return wrapper