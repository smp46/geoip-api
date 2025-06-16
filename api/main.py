"""
FastAPI application for GeoIP lookups.
"""

import logging
import logging.config
from contextlib import asynccontextmanager
from ipaddress import ip_address as IPvAnyAddress
from typing import Optional
import re

from fastapi import Depends, FastAPI, HTTPException, Query, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from api.config import API_DESCRIPTION, API_PREFIX, API_TITLE, API_VERSION
from api.dependencies import get_geoip_lookup
from api.logging_config import get_logging_config
from api.routes import geoip
from geoip_api import GeoIPLookup
from geoip_api.exceptions import InvalidIPError, LookupError

# Configure logging
logging.config.dictConfig(get_logging_config())
logger = logging.getLogger("api")


# Response model
class GeoIPResponse(BaseModel):
    """Response model for GeoIP lookups."""

    ip: str
    code: Optional[str] = None
    country: Optional[str] = None
    continent: Optional[str] = None
    continent_code: Optional[str] = None
    city: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    tz: Optional[str] = None
    currency: Optional[str] = None
    isp: Optional[str] = None
    asn: Optional[int] = None


# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logger.info("Starting GeoIP API service")
    yield
    # Shutdown logic
    logger.info("Shutting down GeoIP API service")


# Create FastAPI application
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    proxy_headers=True,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="api/static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="api/templates")

# Include API routes
app.include_router(geoip.router, prefix=API_PREFIX)


# Simplified IP lookup (domain/ip)
@app.get("/{ip_address}", response_model=GeoIPResponse)
async def lookup_ip_direct(
    ip_address: str,
    geoip_lookup: GeoIPLookup = Depends(get_geoip_lookup),
):
    """
    Look up geolocation information for an IP address using a simplified URL.
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

    except (InvalidIPError, LookupError) as e:
        logger.warning(f"Error with IP: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# Simple query parameter lookup (domain/?ip=x.x.x.x)
@app.get("/", response_model=GeoIPResponse)
async def lookup_ip_query(
    request: Request,
    ip: Optional[str] = Query(None, description="IP address to look up"),
    geoip_lookup: GeoIPLookup = Depends(get_geoip_lookup),
):
    """
    Look up geolocation information using a query parameter.
    Or the requesters IP address, if not otherwise provided.
    """
    try:
        if ip is None:
            # Use requester's IP, if IP not provided
            client = request.client
            if client is not None:
                ip = client.host
            else:
                # Handle the case where client is None
                raise HTTPException(status_code=400, detail="Client IP not available")
            # If IP is a Docker container IP, use X-Forwarded-For header
            if re.match(
                r"\b172\.(1[6-9]|[2-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.\d{1,3}\.\d{1,3}\b",
                ip,
            ):
                ip = request.headers.get("X-Forwarded-For")
                # If IP is still None, return index page
                if ip is None:
                    return templates.TemplateResponse(request, "index.html")

        # Validate IP address format
        IPvAnyAddress(ip)

        # Perform lookup
        result = geoip_lookup.lookup(ip)

        # Add IP address to result
        result["ip"] = ip

        return result

    except ValueError:
        logger.warning(f"Invalid IP address format: {ip}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid IP address format: {ip}",
        )

    except (InvalidIPError, LookupError) as e:
        logger.warning(f"Error with IP: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
