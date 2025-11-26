"""
Unit tests for the YNAB client module.
"""

from unittest import mock

import httpx
import pytest

from src.config import Config
from src.ynab_client import YNABClient, YNABClientError


def create_mock_response(status_code: int, json_data: dict) -> mock.Mock:
    """Create a mock response that properly handles raise_for_status."""
    response = mock.Mock(spec=httpx.Response)
    response.status_code = status_code
    response.json.return_value = json_data
    response.text = str(json_data)

    if status_code >= 400:
        response.raise_for_status.side_effect = httpx.HTTPStatusError(
            f"HTTP {status_code}", request=mock.Mock(), response=response
        )
    else:
        response.raise_for_status.return_value = None

    return response


@pytest.fixture
def config() -> Config:
    """Fixture for test configuration."""
    return Config(ynab_token="test-token", ynab_base_url="https://api.ynab.com/v1")


@pytest.fixture
def client(config: Config) -> YNABClient:
    """Fixture for YNAB client."""
    return YNABClient(config)


class TestYNABClientInit:
    """Tests for YNABClient initialization."""

    def test_client_creation(self, config: Config) -> None:
        """Test that client is created with correct configuration."""
        client = YNABClient(config)
        assert client.config == config
        client.close()

    def test_client_context_manager(self, config: Config) -> None:
        """Test client works as context manager."""
        with YNABClient(config) as client:
            assert client.config == config


class TestYNABClientBudgets:
    """Tests for budget-related API calls."""

    def test_get_budgets(self, client: YNABClient) -> None:
        """Test getting all budgets."""
        mock_response_data = {
            "data": {
                "budgets": [
                    {"id": "budget-1", "name": "My Budget"},
                    {"id": "budget-2", "name": "Another Budget"},
                ]
            }
        }

        with mock.patch.object(
            client._client,
            "get",
            return_value=create_mock_response(200, mock_response_data),
        ):
            result = client.get_budgets()
            assert result == mock_response_data

    def test_get_budget(self, client: YNABClient) -> None:
        """Test getting a single budget."""
        mock_response_data = {
            "data": {
                "budget": {"id": "budget-1", "name": "My Budget"},
            }
        }

        with mock.patch.object(
            client._client,
            "get",
            return_value=create_mock_response(200, mock_response_data),
        ):
            result = client.get_budget("budget-1")
            assert result == mock_response_data

    def test_get_budget_last_used(self, client: YNABClient) -> None:
        """Test getting the last used budget."""
        mock_response_data = {
            "data": {
                "budget": {"id": "budget-1", "name": "My Budget"},
            }
        }

        with mock.patch.object(
            client._client,
            "get",
            return_value=create_mock_response(200, mock_response_data),
        ) as mock_get:
            result = client.get_budget("last-used")
            mock_get.assert_called_once_with("/budgets/last-used", params=None)
            assert result == mock_response_data

    def test_get_budget_settings(self, client: YNABClient) -> None:
        """Test getting budget settings."""
        mock_response_data = {
            "data": {
                "settings": {
                    "currency_format": {"iso_code": "USD"},
                }
            }
        }

        with mock.patch.object(
            client._client,
            "get",
            return_value=create_mock_response(200, mock_response_data),
        ):
            result = client.get_budget_settings("budget-1")
            assert result == mock_response_data


class TestYNABClientAccounts:
    """Tests for account-related API calls."""

    def test_get_accounts(self, client: YNABClient) -> None:
        """Test getting all accounts."""
        mock_response_data = {
            "data": {
                "accounts": [
                    {"id": "account-1", "name": "Checking"},
                    {"id": "account-2", "name": "Savings"},
                ]
            }
        }

        with mock.patch.object(
            client._client,
            "get",
            return_value=create_mock_response(200, mock_response_data),
        ):
            result = client.get_accounts("budget-1")
            assert result == mock_response_data

    def test_get_account(self, client: YNABClient) -> None:
        """Test getting a single account."""
        mock_response_data = {
            "data": {
                "account": {"id": "account-1", "name": "Checking", "balance": 100000},
            }
        }

        with mock.patch.object(
            client._client,
            "get",
            return_value=create_mock_response(200, mock_response_data),
        ):
            result = client.get_account("budget-1", "account-1")
            assert result == mock_response_data


class TestYNABClientTransactions:
    """Tests for transaction-related API calls."""

    def test_get_transactions(self, client: YNABClient) -> None:
        """Test getting transactions."""
        mock_response_data = {
            "data": {
                "transactions": [
                    {"id": "tx-1", "amount": -50000, "payee_name": "Store"},
                ]
            }
        }

        with mock.patch.object(
            client._client,
            "get",
            return_value=create_mock_response(200, mock_response_data),
        ):
            result = client.get_transactions("budget-1")
            assert result == mock_response_data

    def test_get_transactions_with_filters(self, client: YNABClient) -> None:
        """Test getting transactions with filters."""
        mock_response_data = {"data": {"transactions": []}}

        with mock.patch.object(
            client._client,
            "get",
            return_value=create_mock_response(200, mock_response_data),
        ) as mock_get:
            client.get_transactions(
                "budget-1", since_date="2024-01-01", type_filter="uncategorized"
            )
            mock_get.assert_called_once()
            call_args = mock_get.call_args
            assert call_args[0][0] == "/budgets/budget-1/transactions"
            assert call_args[1]["params"] == {
                "since_date": "2024-01-01",
                "type": "uncategorized",
            }

    def test_get_transaction(self, client: YNABClient) -> None:
        """Test getting a single transaction."""
        mock_response_data = {
            "data": {
                "transaction": {"id": "tx-1", "amount": -50000},
            }
        }

        with mock.patch.object(
            client._client,
            "get",
            return_value=create_mock_response(200, mock_response_data),
        ):
            result = client.get_transaction("budget-1", "tx-1")
            assert result == mock_response_data

    def test_get_transactions_by_account(self, client: YNABClient) -> None:
        """Test getting transactions by account."""
        mock_response_data = {"data": {"transactions": []}}

        with mock.patch.object(
            client._client,
            "get",
            return_value=create_mock_response(200, mock_response_data),
        ) as mock_get:
            client.get_transactions_by_account(
                "budget-1", "account-1", since_date="2024-01-01"
            )
            call_args = mock_get.call_args
            assert (
                call_args[0][0]
                == "/budgets/budget-1/accounts/account-1/transactions"
            )
            assert call_args[1]["params"] == {"since_date": "2024-01-01"}


class TestYNABClientCategories:
    """Tests for category-related API calls."""

    def test_get_categories(self, client: YNABClient) -> None:
        """Test getting all categories."""
        mock_response_data = {
            "data": {
                "category_groups": [
                    {"id": "group-1", "name": "Bills", "categories": []},
                ]
            }
        }

        with mock.patch.object(
            client._client,
            "get",
            return_value=create_mock_response(200, mock_response_data),
        ):
            result = client.get_categories("budget-1")
            assert result == mock_response_data

    def test_get_category(self, client: YNABClient) -> None:
        """Test getting a single category."""
        mock_response_data = {
            "data": {
                "category": {"id": "cat-1", "name": "Rent", "budgeted": 150000},
            }
        }

        with mock.patch.object(
            client._client,
            "get",
            return_value=create_mock_response(200, mock_response_data),
        ):
            result = client.get_category("budget-1", "cat-1")
            assert result == mock_response_data


class TestYNABClientErrors:
    """Tests for error handling."""

    def test_http_status_error(self, client: YNABClient) -> None:
        """Test handling of HTTP status errors."""
        mock_response = create_mock_response(401, {"error": {"detail": "Unauthorized"}})

        with mock.patch.object(
            client._client,
            "get",
            return_value=mock_response,
        ):
            with pytest.raises(YNABClientError, match="YNAB API request failed"):
                client.get_budgets()

    def test_request_error(self, client: YNABClient) -> None:
        """Test handling of request errors."""
        with mock.patch.object(
            client._client,
            "get",
            side_effect=httpx.RequestError("Connection failed"),
        ):
            with pytest.raises(YNABClientError, match="YNAB API request failed"):
                client.get_budgets()


class TestYNABClientMonths:
    """Tests for monthly budget API calls."""

    def test_get_months(self, client: YNABClient) -> None:
        """Test getting all months."""
        mock_response_data = {
            "data": {
                "months": [
                    {"month": "2024-01-01", "income": 500000},
                ]
            }
        }

        with mock.patch.object(
            client._client,
            "get",
            return_value=create_mock_response(200, mock_response_data),
        ):
            result = client.get_months("budget-1")
            assert result == mock_response_data

    def test_get_month(self, client: YNABClient) -> None:
        """Test getting a single month."""
        mock_response_data = {
            "data": {
                "month": {"month": "2024-01-01", "income": 500000},
            }
        }

        with mock.patch.object(
            client._client,
            "get",
            return_value=create_mock_response(200, mock_response_data),
        ):
            result = client.get_month("budget-1", "2024-01-01")
            assert result == mock_response_data


class TestYNABClientScheduledTransactions:
    """Tests for scheduled transaction API calls."""

    def test_get_scheduled_transactions(self, client: YNABClient) -> None:
        """Test getting scheduled transactions."""
        mock_response_data = {
            "data": {
                "scheduled_transactions": [
                    {"id": "st-1", "amount": -100000},
                ]
            }
        }

        with mock.patch.object(
            client._client,
            "get",
            return_value=create_mock_response(200, mock_response_data),
        ):
            result = client.get_scheduled_transactions("budget-1")
            assert result == mock_response_data

    def test_get_scheduled_transaction(self, client: YNABClient) -> None:
        """Test getting a single scheduled transaction."""
        mock_response_data = {
            "data": {
                "scheduled_transaction": {"id": "st-1", "amount": -100000},
            }
        }

        with mock.patch.object(
            client._client,
            "get",
            return_value=create_mock_response(200, mock_response_data),
        ):
            result = client.get_scheduled_transaction("budget-1", "st-1")
            assert result == mock_response_data
