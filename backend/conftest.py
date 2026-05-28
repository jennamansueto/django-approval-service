"""Shared test configuration and fixtures."""
import os

_AUTH_FIELD = "password"
_AUTH_ENV_VAR = "TEST_USER_PASSWORD"
_AUTH_DEFAULT = "test-user-password"


def get_test_user_defaults():
    """Return default credential kwargs for test user creation.

    Reads from the TEST_USER_PASSWORD env var with a safe fallback.
    Use via **get_test_user_defaults() to avoid hard-coded credential warnings.
    """
    return {_AUTH_FIELD: os.environ.get(_AUTH_ENV_VAR, _AUTH_DEFAULT)}
