"""Shared constants for the backend test suite.

Centralizes the test-only user password so it isn't hard-coded across
individual test modules. The value is sourced from the ``TEST_USER_PASSWORD``
environment variable when set, with a per-process random fallback so that no
literal credential exists in source.
"""
import os
import secrets

TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD") or secrets.token_urlsafe(16)
