"""Root conftest providing shared test fixtures and constants."""
import os

import pytest

TEST_USER_PASSWORD = os.environ.get("TEST_USER_PASSWORD", "testpass123")
