"""Root conftest providing shared test fixtures and constants."""
import os

import pytest

_FALLBACK = "testpass123"
TEST_USER_PASSWORD = os.environ.get("TEST_USER_PASSWORD", _FALLBACK)
