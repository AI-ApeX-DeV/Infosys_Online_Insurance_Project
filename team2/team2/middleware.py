
from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        excluded_paths = ['/admin/login/', '/login/', '/logout/','/', '/favicon.ico','/login/password_reset_request','/password_reset_verify_otp/']

        print(f"Request path: {request.path}")
        print(f"User authenticated: {request.user.is_authenticated}")

        if not request.user.is_authenticated and request.path not in excluded_paths:
            print(f"Path '{request.path}' is not in excluded paths: {excluded_paths}. Redirecting to login.")
            return redirect(reverse('login'))
        else:
            print(f"Path '{request.path}' is in excluded paths: {excluded_paths}. No redirection.")

        response = self.get_response(request)
        return response