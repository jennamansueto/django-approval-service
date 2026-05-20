"""Shared test configuration and fixtures."""
import os

import pytest

TEST_USER_PASSWORD = os.environ.get('TEST_USER_PASSWORD', 'test-password-not-for-production')


@pytest.fixture
def test_user_password():
    """Return a test password sourced from environment variable."""
    return TEST_USER_PASSWORD
