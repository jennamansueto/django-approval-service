"""Shared test configuration and fixtures."""
import os

TEST_USER_CREDENTIAL = os.environ.get("TEST_USER_PASSWORD", "testpass123")
