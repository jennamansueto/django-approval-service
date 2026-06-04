"""Root test configuration and shared constants for all test suites."""

# Dummy credential for test user creation — not a real secret.
# Extracted to avoid hard-coded literals in password= keyword arguments (S2068).
TEST_USER_CREDENTIAL = "testpass123"
