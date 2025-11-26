"""
Configuration module for YNAB MCP Server.

Handles configuration and token management using environment variables.
"""

import os
from dataclasses import dataclass


@dataclass
class Config:
    """Configuration settings for the YNAB MCP Server."""

    ynab_token: str
    ynab_base_url: str = "https://api.ynab.com/v1"

    @classmethod
    def from_env(cls) -> "Config":
        """
        Create configuration from environment variables.

        Returns:
            Config: Configuration instance with values from environment.

        Raises:
            ValueError: If required environment variables are missing.
        """
        ynab_token = os.environ.get("YNAB_TOKEN")
        if not ynab_token:
            raise ValueError(
                "YNAB_TOKEN environment variable is required. "
                "Please set it to your YNAB personal access token."
            )

        ynab_base_url = os.environ.get("YNAB_BASE_URL", "https://api.ynab.com/v1")

        return cls(ynab_token=ynab_token, ynab_base_url=ynab_base_url)


def get_config() -> Config:
    """
    Get the application configuration.

    Returns:
        Config: Configuration instance.
    """
    return Config.from_env()
