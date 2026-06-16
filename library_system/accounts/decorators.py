from django.http import HttpResponseForbidden
from django.shortcuts import redirect

def librarian_only(view_func):
    """
    Decorator for views that checks if the logged-in user
    explicitly has staff (librarian) access assigned.
    """
    def wrapper_func(request, *args, **kwargs):
        # 1. Ensure the user is actually authenticated
        if not request.user.is_authenticated:
            return redirect('accounts:login')

        # 2. Check the is_staff flag (staff = librarian in this system)
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            # Drop a 403 Forbidden error if a standard student tries to bypass the UI
            return HttpResponseForbidden("Access Denied: You do not have Librarian access permissions.")

    return wrapper_func