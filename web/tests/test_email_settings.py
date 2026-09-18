import logging

from django.conf import settings
from django.core import mail
from django.test import TestCase, override_settings

request_logger = logging.getLogger("django.request")


class EmailSettingsTests(TestCase):
    def test_uses_mailers_instead_of_deprecated_email_settings(self):
        self.assertTrue(hasattr(settings, "MAILERS"))
        for deprecated in (
            "EMAIL_HOST",
            "EMAIL_HOST_USER",
            "EMAIL_HOST_PASSWORD",
            "EMAIL_PORT",
            "EMAIL_USE_SSL",
            "EMAIL_USE_TLS",
        ):
            self.assertFalse(
                hasattr(settings, deprecated),
                f"{deprecated} requested removal: use MAILERS instead",
            )

    def test_mail_admins_handler_is_attached_to_django_logger(self):
        handlers = logging.getLogger("django").handlers
        admin_handlers = [
            handler
            for handler in handlers
            if handler.__class__.__name__ == "AdminEmailHandler"
        ]
        self.assertTrue(admin_handlers, "AdminEmailHandler not wired to django logger")
        self.assertTrue(
            all(getattr(handler, "include_html", False) for handler in admin_handlers),
            "mail_admins handler must include HTML (was dead config)",
        )

    @override_settings(DEBUG=False, ADMINS=["admin@example.com"])
    def test_error_log_email_sent_to_admins_with_html(self):
        try:
            raise ValueError("test error")
        except ValueError:
            request_logger.exception("Test error for admin email")
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertTrue(message.alternatives, "expected HTML alternative in error email")