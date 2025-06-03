"""
API routes for GeoIP lookups.
"""

import logging
from ipaddress import ip_address as IPvAnyAddress
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel

from api.dependencies import get_geoip_lookup
from geoip_api import GeoIPLookup
from geoip_api.exceptions import InvalidIPError, LookupError

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/geoip",
    tags=["geoip"],
)


class GeoIPResponse(BaseModel):
    """Response model for GeoIP lookups."""

    ip: str
    code: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    tz: Optional[str] = None
    currency: Optional[str] = None
    isp: Optional[str] = None
    asn: Optional[int] = None


@router.get(
    "/lookup/{ip_address}",
    response_model=GeoIPResponse,
    summary="Look up geolocation information for an IP address",
    response_description="Geolocation information for the IP address",
)
async def lookup_ip(
    ip_address: str,
    geoip_lookup: GeoIPLookup = Depends(get_geoip_lookup),
) -> Dict[str, Any]:
    """
    Look up geolocation information for an IP address.

    Args:
        ip_address: The IP address to look up

    Returns:
        Geolocation information for the IP address

    Raises:
        HTTPException: If the IP address is invalid or the lookup fails
    """
    try:
        # Validate IP address format
        IPvAnyAddress(ip_address)

        # Perform lookup
        result = geoip_lookup.lookup(ip_address)

        # Add IP address to result
        result["ip"] = ip_address

        return result

    except ValueError:
        logger.warning(f"Invalid IP address format: {ip_address}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid IP address format: {ip_address}",
        )

    except InvalidIPError as e:
        logger.warning(f"Invalid IP address: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except LookupError as e:
        logger.error(f"Lookup error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to look up IP address information",
        )

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )


@router.get(
    "/lookup",
    response_model=GeoIPResponse,
    summary="Look up geolocation information for an IP address (query param)",
    response_description="Geolocation information for the IP address",
)
async def lookup_ip_query(
    ip: str = Query(..., description="The IP address to look up"),
    geoip_lookup: GeoIPLookup = Depends(get_geoip_lookup),
) -> Dict[str, Any]:
    """
    Look up geolocation information for an IP address using a query parameter.

    This endpoint is an alternative to the /lookup/{ip_address} endpoint and accepts
    the IP address as a query parameter instead of a path parameter.

    Args:
        ip: The IP address to look up (query parameter)

    Returns:
        Geolocation information for the IP address
    """
    return await lookup_ip(ip, geoip_lookup)
