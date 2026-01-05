"""
Logging configuration and utilities.
"""

import logging
import os
from datetime import datetime


def setup_logger(name: str = __name__, level: str = "INFO") -> logging.Logger:
    """
    Setup and configure logger.

    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Configured logger instance

    Example:
        logger = setup_logger(__name__, "DEBUG")
        logger.info("Test started")
    """
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(console_formatter)

    # File handler
    log_filename = f"{log_dir}/test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_formatter)

    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def log_test_step(logger: logging.Logger, step: str, details: str = None):
    """
    Log a test step with consistent formatting.

    Args:
        logger: Logger instance
        step: Step description
        details: Optional additional details

    Example:
        log_test_step(logger, "Creating pet", "Pet ID: 12345")
    """
    message = f"STEP: {step}"
    if details:
        message += f" | {details}"
    logger.info(message)


def log_api_request(logger: logging.Logger, method: str, url: str, data: dict = None):
    """
    Log API request details.

    Args:
        logger: Logger instance
        method: HTTP method
        url: Request URL
        data: Request payload

    Example:
        log_api_request(logger, "POST", "/pet", pet_data)
    """
    logger.info(f"API Request: {method} {url}")
    if data:
        logger.debug(f"Request Data: {data}")


def log_api_response(logger: logging.Logger, status_code: int, response_text: str):
    """
    Log API response details.

    Args:
        logger: Logger instance
        status_code: HTTP status code
        response_text: Response body

    Example:
        log_api_response(logger, 200, response.text)
    """
    logger.info(f"API Response: Status {status_code}")
    logger.debug(f"Response Body: {response_text[:500]}")  # First 500 chars
