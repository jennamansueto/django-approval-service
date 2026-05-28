"""Shared test configuration and fixtures."""
import os

import pytest

TEST_USER_PASSWORD = os.environ.get("TEST_USER_PASSWORD", "test-user-password")


@pytest.fixture
def test_password():
    """Return the test user password from environment."""
    return TEST_USER_PASSWORD
