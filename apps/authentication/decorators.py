from django.shortcuts import redirect
from django.contrib import messages


def role_required(*roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")
            if not request.user.is_superuser:
                if request.user.role not in roles:
                    messages.error(
                        request,
                        "You do not have permission to access this page.",
                    )
                    return redirect("dashboard:home")
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def student_required(view_func):
    return role_required("student", "admin")(view_func)


def mentor_required(view_func):
    return role_required("mentor", "admin")(view_func)


def admin_required(view_func):
    return role_required("admin")(view_func)
