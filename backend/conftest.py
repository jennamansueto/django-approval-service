"""Shared test configuration and constants."""
import os
import secrets
import string


def _generate_test_credential():
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(16))


TEST_PASSWORD = os.environ.get("TEST_USER_PASSWORD") or _generate_test_credential()
