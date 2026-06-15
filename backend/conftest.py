"""Shared test configuration and fixtures."""
import os

os.environ.setdefault("TEST_USER_PASSWORD", "testpass123")
TEST_USER_AUTH = os.environ["TEST_USER_PASSWORD"]
