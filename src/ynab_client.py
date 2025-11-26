"""
YNAB API Client module.

Handles all read-only API calls to the YNAB API.
"""

from typing import Any

import httpx

from .config import Config


class YNABClientError(Exception):
    """Custom exception for YNAB API client errors."""

    pass


class YNABClient:
    """
    Client for interacting with the YNAB API.

    Provides read-only access to budgets, accounts, and transactions.
    """

    def __init__(self, config: Config) -> None:
        """
        Initialize the YNAB client.

        Args:
            config: Configuration object containing API token and base URL.
        """
        self.config = config
        self._client = httpx.Client(
            base_url=config.ynab_base_url,
            headers={
                "Authorization": f"Bearer {config.ynab_token}",
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self) -> "YNABClient":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        self.close()

    def _make_request(self, endpoint: str) -> dict[str, Any]:
        """
        Make a GET request to the YNAB API.

        Args:
            endpoint: API endpoint path.

        Returns:
            dict: Parsed JSON response data.

        Raises:
            YNABClientError: If the API request fails.
        """
        try:
            response = self._client.get(endpoint)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise YNABClientError(
                f"YNAB API request failed with status {e.response.status_code}: "
                f"{e.response.text}"
            ) from e
        except httpx.RequestError as e:
            raise YNABClientError(f"YNAB API request failed: {str(e)}") from e

    # Budget endpoints

    def get_budgets(self) -> dict[str, Any]:
        """
        Get all budgets.

        Returns:
            dict: List of budgets and server knowledge.
        """
        return self._make_request("/budgets")

    def get_budget(self, budget_id: str) -> dict[str, Any]:
        """
        Get a single budget by ID.

        Args:
            budget_id: The budget ID or 'last-used' for the last used budget.

        Returns:
            dict: Budget details including accounts, categories, and payees.
        """
        return self._make_request(f"/budgets/{budget_id}")

    def get_budget_settings(self, budget_id: str) -> dict[str, Any]:
        """
        Get budget settings.

        Args:
            budget_id: The budget ID or 'last-used'.

        Returns:
            dict: Budget settings including currency format.
        """
        return self._make_request(f"/budgets/{budget_id}/settings")

    # Account endpoints

    def get_accounts(self, budget_id: str) -> dict[str, Any]:
        """
        Get all accounts for a budget.

        Args:
            budget_id: The budget ID or 'last-used'.

        Returns:
            dict: List of accounts.
        """
        return self._make_request(f"/budgets/{budget_id}/accounts")

    def get_account(self, budget_id: str, account_id: str) -> dict[str, Any]:
        """
        Get a single account by ID.

        Args:
            budget_id: The budget ID or 'last-used'.
            account_id: The account ID.

        Returns:
            dict: Account details.
        """
        return self._make_request(f"/budgets/{budget_id}/accounts/{account_id}")

    # Category endpoints

    def get_categories(self, budget_id: str) -> dict[str, Any]:
        """
        Get all categories for a budget.

        Args:
            budget_id: The budget ID or 'last-used'.

        Returns:
            dict: List of category groups with categories.
        """
        return self._make_request(f"/budgets/{budget_id}/categories")

    def get_category(self, budget_id: str, category_id: str) -> dict[str, Any]:
        """
        Get a single category by ID.

        Args:
            budget_id: The budget ID or 'last-used'.
            category_id: The category ID.

        Returns:
            dict: Category details.
        """
        return self._make_request(f"/budgets/{budget_id}/categories/{category_id}")

    # Payee endpoints

    def get_payees(self, budget_id: str) -> dict[str, Any]:
        """
        Get all payees for a budget.

        Args:
            budget_id: The budget ID or 'last-used'.

        Returns:
            dict: List of payees.
        """
        return self._make_request(f"/budgets/{budget_id}/payees")

    def get_payee(self, budget_id: str, payee_id: str) -> dict[str, Any]:
        """
        Get a single payee by ID.

        Args:
            budget_id: The budget ID or 'last-used'.
            payee_id: The payee ID.

        Returns:
            dict: Payee details.
        """
        return self._make_request(f"/budgets/{budget_id}/payees/{payee_id}")

    # Transaction endpoints

    def get_transactions(
        self,
        budget_id: str,
        since_date: str | None = None,
        type_filter: str | None = None,
    ) -> dict[str, Any]:
        """
        Get transactions for a budget.

        Args:
            budget_id: The budget ID or 'last-used'.
            since_date: Optional filter for transactions since a date (YYYY-MM-DD).
            type_filter: Optional filter by transaction type
                ('uncategorized', 'unapproved').

        Returns:
            dict: List of transactions.
        """
        params = {}
        if since_date:
            params["since_date"] = since_date
        if type_filter:
            params["type"] = type_filter

        endpoint = f"/budgets/{budget_id}/transactions"
        if params:
            param_str = "&".join(f"{k}={v}" for k, v in params.items())
            endpoint = f"{endpoint}?{param_str}"

        return self._make_request(endpoint)

    def get_transaction(self, budget_id: str, transaction_id: str) -> dict[str, Any]:
        """
        Get a single transaction by ID.

        Args:
            budget_id: The budget ID or 'last-used'.
            transaction_id: The transaction ID.

        Returns:
            dict: Transaction details.
        """
        return self._make_request(f"/budgets/{budget_id}/transactions/{transaction_id}")

    def get_transactions_by_account(
        self,
        budget_id: str,
        account_id: str,
        since_date: str | None = None,
    ) -> dict[str, Any]:
        """
        Get transactions for a specific account.

        Args:
            budget_id: The budget ID or 'last-used'.
            account_id: The account ID.
            since_date: Optional filter for transactions since a date (YYYY-MM-DD).

        Returns:
            dict: List of transactions for the account.
        """
        endpoint = f"/budgets/{budget_id}/accounts/{account_id}/transactions"
        if since_date:
            endpoint = f"{endpoint}?since_date={since_date}"

        return self._make_request(endpoint)

    def get_transactions_by_category(
        self,
        budget_id: str,
        category_id: str,
        since_date: str | None = None,
    ) -> dict[str, Any]:
        """
        Get transactions for a specific category.

        Args:
            budget_id: The budget ID or 'last-used'.
            category_id: The category ID.
            since_date: Optional filter for transactions since a date (YYYY-MM-DD).

        Returns:
            dict: List of transactions for the category.
        """
        endpoint = f"/budgets/{budget_id}/categories/{category_id}/transactions"
        if since_date:
            endpoint = f"{endpoint}?since_date={since_date}"

        return self._make_request(endpoint)

    def get_transactions_by_payee(
        self,
        budget_id: str,
        payee_id: str,
        since_date: str | None = None,
    ) -> dict[str, Any]:
        """
        Get transactions for a specific payee.

        Args:
            budget_id: The budget ID or 'last-used'.
            payee_id: The payee ID.
            since_date: Optional filter for transactions since a date (YYYY-MM-DD).

        Returns:
            dict: List of transactions for the payee.
        """
        endpoint = f"/budgets/{budget_id}/payees/{payee_id}/transactions"
        if since_date:
            endpoint = f"{endpoint}?since_date={since_date}"

        return self._make_request(endpoint)

    # Monthly budget endpoints

    def get_months(self, budget_id: str) -> dict[str, Any]:
        """
        Get all budget months.

        Args:
            budget_id: The budget ID or 'last-used'.

        Returns:
            dict: List of budget months.
        """
        return self._make_request(f"/budgets/{budget_id}/months")

    def get_month(self, budget_id: str, month: str) -> dict[str, Any]:
        """
        Get a single budget month.

        Args:
            budget_id: The budget ID or 'last-used'.
            month: The month in YYYY-MM-DD format (day will be ignored).

        Returns:
            dict: Budget month details including category balances.
        """
        return self._make_request(f"/budgets/{budget_id}/months/{month}")

    # Scheduled transactions

    def get_scheduled_transactions(self, budget_id: str) -> dict[str, Any]:
        """
        Get all scheduled transactions.

        Args:
            budget_id: The budget ID or 'last-used'.

        Returns:
            dict: List of scheduled transactions.
        """
        return self._make_request(f"/budgets/{budget_id}/scheduled_transactions")

    def get_scheduled_transaction(
        self, budget_id: str, scheduled_transaction_id: str
    ) -> dict[str, Any]:
        """
        Get a single scheduled transaction.

        Args:
            budget_id: The budget ID or 'last-used'.
            scheduled_transaction_id: The scheduled transaction ID.

        Returns:
            dict: Scheduled transaction details.
        """
        return self._make_request(
            f"/budgets/{budget_id}/scheduled_transactions/{scheduled_transaction_id}"
        )
