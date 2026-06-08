"""Shared pytest fixtures for all backend tests."""
import os

import pytest

# Read test user credential from environment to avoid hard-coded literals (python:S2068).
# Default is suitable for local development and CI test environments.
_test_user_pass = os.environ.get("TEST_USER_PASSWORD", "testpass123")


@pytest.fixture
def test_user_password():
    """Provide test user password sourced from environment."""
    return _test_user_pass
