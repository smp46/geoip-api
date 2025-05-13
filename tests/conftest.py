"""
Pytest fixtures and configuration.
"""

from pathlib import Path

import pytest

from geoip_api import GeoIPLookup

# Test data
TEST_IP_GOOGLE_DNS = "8.8.8.8"
TEST_IP_CLOUDFLARE = "1.1.1.1"
TEST_IP_INVALID = "999.999.999.999"


@pytest.fixture
def mock_db_paths(monkeypatch, tmp_path):
    """Mock database paths for testing."""
    city_db = tmp_path / "GeoLite2-City.mmdb"
    asn_db = tmp_path / "GeoLite2-ASN.mmdb"

    # Create empty files to simulate database files
    city_db.write_text("")
    asn_db.write_text("")

    monkeypatch.setattr("geoip_api.config.DEFAULT_CITY_DB_PATH", str(city_db))
    monkeypatch.setattr("geoip_api.config.DEFAULT_ASN_DB_PATH", str(asn_db))

    return {"city": str(city_db), "asn": str(asn_db)}


@pytest.fixture
def real_db_paths():
    """Get paths to real database files for testing with real data."""
    home_dir = Path.home()
    db_dir = home_dir / ".geoip_api"

    city_db = db_dir / "GeoLite2-City.mmdb"
    asn_db = db_dir / "GeoLite2-ASN.mmdb"

    # Skip tests that need real databases if they don't exist
    if not city_db.exists() or not asn_db.exists():
        pytest.skip("Real database files not available")

    return {"city": str(city_db), "asn": str(asn_db)}


@pytest.fixture
def geoip_lookup(real_db_paths):
    """Return a GeoIPLookup instance using real databases."""
    return GeoIPLookup(
        city_db_path=real_db_paths["city"], asn_db_path=real_db_paths["asn"]
    )
