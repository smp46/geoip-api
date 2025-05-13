"""
Logging configuration for the FastAPI application.
"""

import logging
from typing import Any, Dict

LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def get_logging_config() -> Dict[str, Any]:
    """
    Get logging configuration dictionary.
    """
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": LOG_FORMAT,
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": LOG_LEVEL,
                "formatter": "default",
            },
        },
        "loggers": {
            "api": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
            "geoip_api": {
                "handlers": ["console"],
                "level": LOG_LEVEL,
                "propagate": False,
            },
            "uvicorn": {
                "handlers": ["console"],
                "level": LOG_LEVEL,
                "propagate": False,
            },
            "fastapi": {
                "handlers": ["console"],
                "level": LOG_LEVEL,
                "propagate": False,
            },
        },
        "root": {"handlers": ["console"], "level": LOG_LEVEL},
    }
