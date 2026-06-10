"""Shared test configuration and constants."""
import os

TEST_USER_CREDENTIAL = os.environ.get("DJANGO_TEST_USER_CREDENTIAL", "testpass123")
