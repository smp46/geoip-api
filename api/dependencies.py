"""
FastAPI dependencies for the GeoIP API.
"""

import logging
import os
from functools import lru_cache

import requests
from fastapi import Depends, HTTPException, status

from api.config import ASN_DB_PATH, ASN_DB_URL, CITY_DB_PATH, CITY_DB_URL, DB_DIR
from geoip_api import GeoIPLookup

logger = logging.getLogger(__name__)


@lru_cache()
def ensure_databases():
    """
    Ensure database files exist, downloading them if necessary.

    This function is cached to avoid repeated checks in a single application instance.
    """
    logger.info("Checking for GeoIP database files")

    # Ensure the database directory exists
    os.makedirs(DB_DIR, exist_ok=True)

    # Download databases if they don't exist
    if not os.path.exists(CITY_DB_PATH):
        logger.info(f"City database not found at {CITY_DB_PATH}, downloading...")
        try:
            response = requests.get(
                CITY_DB_URL, stream=True, timeout=60, allow_redirects=True
            )
            response.raise_for_status()
            with open(CITY_DB_PATH, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            logger.info(f"Successfully downloaded City database to {CITY_DB_PATH}")
        except Exception as e:
            logger.error(f"Failed to download city database: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to download required database files",
            )

    if not os.path.exists(ASN_DB_PATH):
        logger.info(f"ASN database not found at {ASN_DB_PATH}, downloading...")
        try:
            response = requests.get(
                ASN_DB_URL, stream=True, timeout=60, allow_redirects=True
            )
            response.raise_for_status()
            with open(ASN_DB_PATH, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            logger.info(f"Successfully downloaded ASN database to {ASN_DB_PATH}")
        except Exception as e:
            logger.error(f"Failed to download ASN database: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to download required database files",
            )

    logger.info("Database files are available")
    return True


def get_geoip_lookup(databases_ready: bool = Depends(ensure_databases)):
    """
    Get a GeoIPLookup instance as a FastAPI dependency.
    """
    try:
        return GeoIPLookup(city_db_path=CITY_DB_PATH, asn_db_path=ASN_DB_PATH)
    except Exception as e:
        logger.error(f"Failed to initialize GeoIPLookup: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initialize GeoIP service",
        )
