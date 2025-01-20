import datetime
import logging
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
