"""Shared test configuration and fixtures."""
import os
import uuid

import pytest

TEST_PASSWORD = os.environ.get("TEST_USER_PASSWORD") or f"test-{uuid.uuid4().hex[:16]}"


@pytest.fixture
def test_password():
    """Return the test password from environment variable."""
    return TEST_PASSWORD
