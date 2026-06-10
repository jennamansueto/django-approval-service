"""Shared test configuration and constants."""
import os

TEST_USER_PASSWORD = os.environ.get("DJANGO_TEST_USER_PASSWORD", "testpass123")
