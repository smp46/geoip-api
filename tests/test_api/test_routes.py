"""
Tests for the FastAPI routes.
"""

from fastapi.testclient import TestClient

from api.main import app
from tests.conftest import TEST_IP_GOOGLE_DNS, TEST_IP_INVALID

client = TestClient(app)


def test_index_page():
    """Test the index page."""
    response = client.get("/")
    assert response.status_code == 200
    assert "GeoIP API" in response.text


def test_lookup_endpoint_valid_ip():
    """Test the lookup endpoint with a valid IP."""
    response = client.get(f"/api/v1/geoip/lookup/{TEST_IP_GOOGLE_DNS}")
    assert response.status_code == 200

    data = response.json()
    assert data["ip"] == TEST_IP_GOOGLE_DNS
    assert "country" in data
    assert "city" in data
    assert "lat" in data
    assert "lon" in data
    assert "isp" in data
    assert "asn" in data


def test_lookup_endpoint_invalid_ip():
    """Test the lookup endpoint with an invalid IP."""
    response = client.get(f"/api/v1/geoip/lookup/{TEST_IP_INVALID}")
    assert response.status_code == 400


def test_lookup_query_endpoint_valid_ip():
    """Test the lookup query endpoint with a valid IP."""
    response = client.get(f"/api/v1/geoip/lookup?ip={TEST_IP_GOOGLE_DNS}")
    assert response.status_code == 200

    data = response.json()
    assert data["ip"] == TEST_IP_GOOGLE_DNS
    assert "country" in data
    assert "city" in data


def test_lookup_query_endpoint_missing_param():
    """Test the lookup query endpoint with a missing IP parameter."""
    response = client.get("/api/v1/geoip/lookup")
    assert response.status_code == 422  # Validation error
