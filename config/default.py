"""
Default configurations.
"""

DEBUG = False

# Default is 12.
# Take around 300ms on Vultr 768MiB VPS.
BCRYPT_LOG_ROUNDS = 12

# Expire in 30 days.
AUTH_TOKEN_EXPIRATION = 30 * 24 * 3600

