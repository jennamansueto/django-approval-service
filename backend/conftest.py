"""Shared test configuration and fixtures."""
import os
import secrets

import pytest


def _generate_test_credential():
    """Generate a random credential for use in tests."""
    return secrets.token_urlsafe(16)


TEST_USER_PASSWORD = os.environ.get('TEST_USER_PASSWORD') or _generate_test_credential()


@pytest.fixture
def test_user_password():
    """Return a test credential sourced from environment variable."""
    return TEST_USER_PASSWORD
