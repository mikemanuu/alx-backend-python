import datetime


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
