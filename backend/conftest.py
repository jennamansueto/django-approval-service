"""Shared test configuration and fixtures."""
import os

import pytest

TEST_PASSWORD = os.environ.get("TEST_USER_PASSWORD", "test-placeholder-pass")


@pytest.fixture
def test_password():
    """Return the test password from environment variable."""
    return TEST_PASSWORD
