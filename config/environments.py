"""
Environment configuration management.
Supports dev, qa, staging, and production environments.
"""

import os
from enum import Enum
from typing import Dict, Any


class Environment(Enum):
    """Supported test environments"""

    DEV = "dev"
    QA = "qa"
    STAGING = "staging"
    PROD = "prod"


class Config:
    """
    Environment-specific configuration management.

    Usage:
        config = Config.get_config("qa")
        base_url = config["base_url"]
    """

    ENVIRONMENTS: Dict[str, Dict[str, Any]] = {
        "dev": {
            "base_url": "https://petstore-dev.swagger.io/v2",
            "timeout": 10,
            "retry_count": 3,
            "parallel_workers": 4,
            "log_level": "DEBUG",
        },
        "qa": {
            "base_url": "https://petstore.swagger.io/v2",
            "timeout": 15,
            "retry_count": 2,
            "parallel_workers": 4,
            "log_level": "INFO",
        },
        "staging": {
            "base_url": "https://petstore-staging.swagger.io/v2",
            "timeout": 20,
            "retry_count": 2,
            "parallel_workers": 2,
            "log_level": "INFO",
        },
        "prod": {
            "base_url": "https://petstore.swagger.io/v2",
            "timeout": 30,
            "retry_count": 1,
            "parallel_workers": 1,
            "log_level": "WARNING",
        },
    }

    @classmethod
    def get_config(cls, env: str = None) -> Dict[str, Any]:
        """
        Get configuration for specified environment.

        Args:
            env: Environment name (dev/qa/staging/prod)

        Returns:
            Dictionary with environment configuration

        Defaults to QA if environment not specified or invalid.
        """
        env = env or os.getenv("TEST_ENV", "qa")
        env = env.lower()

        if env not in cls.ENVIRONMENTS:
            print(f"Warning: Unknown environment '{env}', defaulting to 'qa'")
            env = "qa"

        return cls.ENVIRONMENTS[env].copy()

    @classmethod
    def get_base_url(cls, env: str = None) -> str:
        """Get base URL for environment"""
        config = cls.get_config(env)
        return config["base_url"]

    @classmethod
    def get_timeout(cls, env: str = None) -> int:
        """Get timeout value for environment"""
        config = cls.get_config(env)
        return config["timeout"]
