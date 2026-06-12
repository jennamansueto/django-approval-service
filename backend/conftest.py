"""Shared test configuration for all backend test modules."""
import os
import uuid

TEST_USER_PASSWORD = os.environ.get("DJANGO_TEST_USER_PASSWORD") or f"test-{uuid.uuid4().hex}"
