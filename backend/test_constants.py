"""Shared constants for test suites.

Centralises test credentials so they are not hard-coded as literals in
individual test files (SonarQube python:S2068).
"""
import os

TEST_USER_CREDENTIAL = os.environ.get("TEST_USER_CREDENTIAL", "testpass123")
