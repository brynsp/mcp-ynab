"""
Unit tests for the MCP server main module.
"""

import json
from unittest import mock

import pytest

from src.config import Config
from src.main import _execute_tool, format_response, list_tools
from src.ynab_client import YNABClient


class TestFormatResponse:
    """Tests for the format_response function."""

    def test_format_simple_dict(self) -> None:
        """Test formatting a simple dictionary."""
        data = {"key": "value"}
        result = format_response(data)
        assert json.loads(result) == data

    def test_format_nested_dict(self) -> None:
        """Test formatting a nested dictionary."""
        data = {"data": {"budgets": [{"id": "1", "name": "Test"}]}}
        result = format_response(data)
        assert json.loads(result) == data


class TestListTools:
    """Tests for the list_tools function."""

    @pytest.mark.asyncio
    async def test_list_tools_returns_tools(self) -> None:
        """Test that list_tools returns a list of tools."""
        tools = await list_tools()
        assert len(tools) > 0

    @pytest.mark.asyncio
    async def test_list_tools_contains_get_budgets(self) -> None:
        """Test that list_tools contains get_budgets tool."""
        tools = await list_tools()
        tool_names = [tool.name for tool in tools]
        assert "get_budgets" in tool_names

    @pytest.mark.asyncio
    async def test_list_tools_contains_required_tools(self) -> None:
        """Test that list_tools contains all expected tools."""
        tools = await list_tools()
        tool_names = [tool.name for tool in tools]

        expected_tools = [
            "get_budgets",
            "get_budget",
            "get_accounts",
            "get_account",
            "get_categories",
            "get_category",
            "get_payees",
            "get_payee",
            "get_transactions",
            "get_transaction",
            "get_months",
            "get_month",
            "get_scheduled_transactions",
            "get_scheduled_transaction",
        ]

        for tool_name in expected_tools:
            assert tool_name in tool_names, f"Expected tool {tool_name} not found"

    @pytest.mark.asyncio
    async def test_tools_have_descriptions(self) -> None:
        """Test that all tools have descriptions."""
        tools = await list_tools()
        for tool in tools:
            assert tool.description, f"Tool {tool.name} has no description"

    @pytest.mark.asyncio
    async def test_tools_have_input_schemas(self) -> None:
        """Test that all tools have input schemas."""
        tools = await list_tools()
        for tool in tools:
            assert tool.inputSchema, f"Tool {tool.name} has no input schema"


class TestExecuteTool:
    """Tests for the _execute_tool function."""

    @pytest.fixture
    def config(self) -> Config:
        """Fixture for test configuration."""
        return Config(ynab_token="test-token")

    @pytest.fixture
    def client(self, config: Config) -> YNABClient:
        """Fixture for YNAB client."""
        return YNABClient(config)

    @pytest.mark.asyncio
    async def test_execute_get_budgets(self, client: YNABClient) -> None:
        """Test executing get_budgets tool."""
        mock_response = {"data": {"budgets": []}}

        with mock.patch.object(client, "get_budgets", return_value=mock_response):
            result = await _execute_tool(client, "get_budgets", {})
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_execute_get_budget(self, client: YNABClient) -> None:
        """Test executing get_budget tool."""
        mock_response = {"data": {"budget": {"id": "budget-1"}}}

        with mock.patch.object(client, "get_budget", return_value=mock_response):
            result = await _execute_tool(
                client, "get_budget", {"budget_id": "budget-1"}
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_execute_get_accounts(self, client: YNABClient) -> None:
        """Test executing get_accounts tool."""
        mock_response = {"data": {"accounts": []}}

        with mock.patch.object(client, "get_accounts", return_value=mock_response):
            result = await _execute_tool(
                client, "get_accounts", {"budget_id": "budget-1"}
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_execute_get_transactions_with_filters(
        self, client: YNABClient
    ) -> None:
        """Test executing get_transactions with filters."""
        mock_response = {"data": {"transactions": []}}

        with mock.patch.object(
            client, "get_transactions", return_value=mock_response
        ) as mock_get:
            result = await _execute_tool(
                client,
                "get_transactions",
                {
                    "budget_id": "budget-1",
                    "since_date": "2024-01-01",
                    "type": "uncategorized",
                },
            )
            mock_get.assert_called_once_with(
                "budget-1", since_date="2024-01-01", type_filter="uncategorized"
            )
            assert result == mock_response

    @pytest.mark.asyncio
    async def test_execute_unknown_tool(self, client: YNABClient) -> None:
        """Test executing unknown tool raises ValueError."""
        with pytest.raises(ValueError, match="Unknown tool"):
            await _execute_tool(client, "unknown_tool", {})
