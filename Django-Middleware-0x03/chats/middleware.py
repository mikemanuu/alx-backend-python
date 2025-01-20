from datetime import datetime, timedelta
import logging
from django.http import JsonResponse
from django.http import HttpResponseForbidden


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the user (or 'Anonymous' if not authenticated)
        user = request.user if request.user.is_authenticated else "Anonymous"

        # Log the request information
        log_message = f"{datetime.datetime.now()} - User: {user} - Path: {request.path}\n"
        with open("user_requests.log", "a") as log_file:  # Appending logs to a file
            log_file.write(log_message)

        # Process the request
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the current server time (24-hour format)
        current_hour = datetime.datetime.now().hour

        # Deny access if the time is outside 9 PM to 6 PM (21:00 to 18:00)
        if current_hour < 18 or current_hour >= 21:
            return HttpResponseForbidden("Access to the chat is restricted at this time.")

        # Continue processing the request
        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Store user activity by IP
        self.ip_message_tracker = {}

    def __call__(self, request):
        # Only process POST requests (assume these are chat messages)
        if request.method == "POST":
            # Get user's IP address
            ip_address = self.get_client_ip(request)

            # Initialize or update user's activity
            now = datetime.now()
            if ip_address not in self.ip_message_tracker:
                self.ip_message_tracker[ip_address] = []

            # Remove messages older than 1 minute
            self.ip_message_tracker[ip_address] = [
                timestamp for timestamp in self.ip_message_tracker[ip_address]
                if now - timestamp < timedelta(minutes=1)
            ]

            # Check if limit is exceeded
            if len(self.ip_message_tracker[ip_address]) >= 5:
                return JsonResponse(
                    {"error": "Message limit exceeded. Try again after a minute."},
                    status=429
                )

            # Add the current timestamp to the tracker
            self.ip_message_tracker[ip_address].append(now)

            # Optional: Detect offensive language (for demonstration purposes, we check for specific words)
            offensive_words = {"badword1", "badword2",
                               "badword3"}  # Add actual words
            message_content = request.POST.get("message", "").lower()
            if any(offensive_word in message_content for offensive_word in offensive_words):
                return JsonResponse(
                    {"error": "Offensive language detected. Message blocked."},
                    status=400
                )

        # Process the request
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Retrieve the client's IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request path requires role permissions
        # Define paths that need admin or moderator roles
        protected_paths = ["/chat/manage/", "/chat/admin/"]
        if request.path in protected_paths:
            # Get user role from request (assuming the role is stored in session or user object)
            # Replace with your role retrieval logic
            user_role = request.session.get("role", None)

            # Check if the user role is 'admin' or 'moderator'
            if user_role not in {"admin", "moderator"}:
                return HttpResponseForbidden("Access denied: insufficient permissions.")

        # Allow the request to proceed
        response = self.get_response(request)
        return response
