"""
Unit tests for the configuration module.
"""

import os
from unittest import mock

import pytest

from src.config import Config, get_config


class TestConfig:
    """Tests for the Config class."""

    def test_from_env_success(self) -> None:
        """Test successful configuration from environment variables."""
        with mock.patch.dict(os.environ, {"YNAB_TOKEN": "test-token"}):
            config = Config.from_env()
            assert config.ynab_token == "test-token"
            assert config.ynab_base_url == "https://api.ynab.com/v1"

    def test_from_env_custom_base_url(self) -> None:
        """Test configuration with custom base URL."""
        with mock.patch.dict(
            os.environ,
            {"YNAB_TOKEN": "test-token", "YNAB_BASE_URL": "https://custom.api.com"},
        ):
            config = Config.from_env()
            assert config.ynab_token == "test-token"
            assert config.ynab_base_url == "https://custom.api.com"

    def test_from_env_missing_token(self) -> None:
        """Test that missing token raises ValueError."""
        with mock.patch.dict(os.environ, {}, clear=True):
            # Ensure YNAB_TOKEN is not set
            os.environ.pop("YNAB_TOKEN", None)
            with pytest.raises(
                ValueError, match="YNAB_TOKEN environment variable is required"
            ):
                Config.from_env()

    def test_config_dataclass(self) -> None:
        """Test Config dataclass creation."""
        config = Config(ynab_token="my-token", ynab_base_url="https://api.example.com")
        assert config.ynab_token == "my-token"
        assert config.ynab_base_url == "https://api.example.com"

    def test_config_default_base_url(self) -> None:
        """Test Config default base URL."""
        config = Config(ynab_token="my-token")
        assert config.ynab_base_url == "https://api.ynab.com/v1"


class TestGetConfig:
    """Tests for the get_config function."""

    def test_get_config_returns_config_instance(self) -> None:
        """Test that get_config returns a Config instance."""
        with mock.patch.dict(os.environ, {"YNAB_TOKEN": "test-token"}):
            config = get_config()
            assert isinstance(config, Config)
            assert config.ynab_token == "test-token"
