from django.test import TestCase, RequestFactory
from django.db.utils import OperationalError
from django.http import HttpResponse
from web.middleware import DatabaseDownMiddleware
from unittest.mock import Mock

class TestDatabaseDownMiddleware(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_middleware_passes_through_normal_response(self):
        get_response = Mock(return_value=HttpResponse("OK"))
        middleware = DatabaseDownMiddleware(get_response)
        request = self.factory.get('/')
        response = middleware(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"OK")

    def test_middleware_catches_operational_error(self):
        get_response = Mock(side_effect=OperationalError("Database is down"))
        middleware = DatabaseDownMiddleware(get_response)
        request = self.factory.get('/')
        response = middleware(request)
        self.assertEqual(response.status_code, 500)
        # Check if the error500.html template was used
        self.assertContains(response, "We’ll be back soon!", status_code=500)
