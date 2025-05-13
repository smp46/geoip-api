"""
Configuration for the FastAPI application.
"""

import os
from pathlib import Path

# API settings
API_TITLE = "GeoIP API"
API_DESCRIPTION = """
A REST API for GeoIP lookups. This API allows you to lookup geographic 
and network information for IP addresses using the MaxMind GeoLite2 databases.
"""
API_VERSION = "1.0.1"
API_PREFIX = "/api/v1"

# Database settings
DB_DIR = Path(__file__).parent / "db"
CITY_DB_PATH = os.environ.get("GEOIP_CITY_DB_PATH", str(DB_DIR / "GeoLite2-City.mmdb"))
ASN_DB_PATH = os.environ.get("GEOIP_ASN_DB_PATH", str(DB_DIR / "GeoLite2-ASN.mmdb"))

# Database download URLs
ASN_DB_URL = "https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-ASN.mmdb"
CITY_DB_URL = "https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-City.mmdb"

# Limits and caching
RATE_LIMIT = int(os.environ.get("RATE_LIMIT", "100"))  # requests per minute
CACHE_TTL = int(os.environ.get("CACHE_TTL", "3600"))  # seconds
