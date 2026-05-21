"""Shared test configuration and fixtures."""
import os

import pytest

TEST_USER_CREDENTIAL = os.environ.get("DJANGO_TEST_USER_PASSWORD", "testpass123")


@pytest.fixture
def test_password():
    """Return the test user password."""
    return TEST_USER_CREDENTIAL
