# web/middleware.py
from django.db.utils import OperationalError
from django.shortcuts import render
from django.http import HttpResponseServerError

class DatabaseDownMiddleware:
    """
    Catch database OperationalError and show custom 500 error page.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except OperationalError:
            # Render error500.html template
            return HttpResponseServerError(render(request, "error500.html"))