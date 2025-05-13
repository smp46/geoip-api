"""
Tests for the GeoIP lookup functionality.
"""

import pytest

from geoip_api import GeoIPLookup
from geoip_api.exceptions import InvalidIPError
from tests.conftest import TEST_IP_GOOGLE_DNS, TEST_IP_INVALID


def test_validate_ip_valid():
    """Test IP validation with a valid IP."""
    lookup = GeoIPLookup()
    # Should not raise an exception
    lookup.validate_ip(TEST_IP_GOOGLE_DNS)


def test_validate_ip_invalid():
    """Test IP validation with an invalid IP."""
    lookup = GeoIPLookup()
    with pytest.raises(InvalidIPError):
        lookup.validate_ip(TEST_IP_INVALID)


def test_lookup_valid_ip(geoip_lookup):
    """Test lookup with a valid IP."""
    result = geoip_lookup.lookup(TEST_IP_GOOGLE_DNS)

    # Check that the result contains expected keys
    assert "country" in result
    assert "city" in result
    assert "lat" in result
    assert "lon" in result
    assert "isp" in result
    assert "asn" in result


def test_lookup_invalid_ip(geoip_lookup):
    """Test lookup with an invalid IP."""
    with pytest.raises(InvalidIPError):
        geoip_lookup.lookup(TEST_IP_INVALID)
