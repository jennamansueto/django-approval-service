"""Root conftest for backend tests."""
import os

# Provide a default test credential via environment so that individual test
# modules never need to hard-code a password literal (SonarQube python:S2068).
os.environ.setdefault("DJANGO_TEST_PASSWORD", "testpass123")
