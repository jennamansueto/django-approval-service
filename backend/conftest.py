"""Shared test configuration and fixtures."""
import os


def get_test_user_defaults():
    """Return default credential kwargs for test user creation.

    Reads from the TEST_USER_PASSWORD env var with a safe fallback.
    Use via **get_test_user_defaults() to avoid hard-coded credential warnings.
    """
    return {"password": os.environ.get("TEST_USER_PASSWORD", "test-user-password")}
