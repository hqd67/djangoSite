from django.shortcuts import redirect

def blog_login_required(func):
    def wrapper(request, *args, **kwargs):
        if "blog_user_id" not in request.session:
            return redirect("blog_login")
        return func(request, *args, **kwargs)
    return wrapper
