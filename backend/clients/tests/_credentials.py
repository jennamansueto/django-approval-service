"""Shared test credential helpers for the clients app.

Avoids hard-coded password literals in test fixtures (SonarQube python:S2068).
Reads ``TEST_USER_PASSWORD`` from the environment when supplied (e.g. in CI),
otherwise generates a fresh random value for the test session.
"""
import os
import secrets

TEST_USER_PASSWORD = os.environ.get("TEST_USER_PASSWORD") or secrets.token_urlsafe(16)
