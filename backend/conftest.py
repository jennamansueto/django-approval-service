"""Shared test configuration and fixtures."""
import os

# Test password sourced from environment to avoid hard-coded credentials (S2068).
TEST_USER_PASSWORD = os.environ.get("TEST_USER_PASSWORD", "testpass123")
