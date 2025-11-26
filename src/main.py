"""
YNAB MCP Server Entry Point.

This module implements the MCP (Model Context Protocol) server that exposes
YNAB API read-only operations as tools.
"""

import json
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from .config import get_config
from .ynab_client import YNABClient, YNABClientError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create the MCP server
server = Server("ynab-mcp-server")


def get_ynab_client() -> YNABClient:
    """Get a YNAB client instance."""
    config = get_config()
    return YNABClient(config)


def format_response(data: dict[str, Any]) -> str:
    """Format API response data as JSON string."""
    return json.dumps(data, indent=2)


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available YNAB tools."""
    return [
        Tool(
            name="get_budgets",
            description="Get all budgets associated with the YNAB account",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="get_budget",
            description=(
                "Get a single budget by ID. "
                "Use 'last-used' for the most recently accessed budget."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "budget_id": {
                        "type": "string",
                        "description": "The budget ID or 'last-used'",
                    }
                },
                "required": ["budget_id"],
            },
        ),
        Tool(
            name="get_budget_settings",
            description="Get settings for a budget including currency format",
            inputSchema={
                "type": "object",
                "properties": {
                    "budget_id": {
                        "type": "string",
                        "description": "The budget ID or 'last-used'",
                    }
                },
                "required": ["budget_id"],
            },
        ),
        Tool(
            name="get_accounts",
            description="Get all accounts for a budget",
            inputSchema={
                "type": "object",
                "properties": {
                    "budget_id": {
                        "type": "string",
                        "description": "The budget ID or 'last-used'",
                    }
                },
                "required": ["budget_id"],
            },
        ),
        Tool(
            name="get_account",
            description="Get a single account by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "budget_id": {
                        "type": "string",
                        "description": "The budget ID or 'last-used'",
                    },
                    "account_id": {
                        "type": "string",
                        "description": "The account ID",
                    },
                },
                "required": ["budget_id", "account_id"],
            },
        ),
        Tool(
            name="get_categories",
            description="Get all categories for a budget",
            inputSchema={
                "type": "object",
                "properties": {
                    "budget_id": {
                        "type": "string",
                        "description": "The budget ID or 'last-used'",
                    }
                },
                "required": ["budget_id"],
            },
        ),
        Tool(
            name="get_category",
            description="Get a single category by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "budget_id": {
                        "type": "string",
                        "description": "The budget ID or 'last-used'",
                    },
                    "category_id": {
                        "type": "string",
                        "description": "The category ID",
                    },
                },
                "required": ["budget_id", "category_id"],
            },
        ),
        Tool(
            name="get_payees",
            description="Get all payees for a budget",
            inputSchema={
                "type": "object",
                "properties": {
                    "budget_id": {
                        "type": "string",
                        "description": "The budget ID or 'last-used'",
                    }
                },
                "required": ["budget_id"],
            },
        ),
        Tool(
            name="get_payee",
            description="Get a single payee by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "budget_id": {
                        "type": "string",
                        "description": "The budget ID or 'last-used'",
                    },
                    "payee_id": {
                        "type": "string",
                        "description": "The payee ID",
                    },
                },
                "required": ["budget_id", "payee_id"],
            },
        ),
        Tool(
            name="get_transactions",
            description=(
                "Get transactions for a budget. "
                "Optionally filter by date or type."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "budget_id": {
                        "type": "string",
                        "description": "The budget ID or 'last-used'",
                    },
                    "since_date": {
                        "type": "string",
                        "description": (
                            "Filter transactions since this date (YYYY-MM-DD)"
                        ),
                    },
                    "type": {
                        "type": "string",
                        "description": (
                            "Filter by type: 'uncategorized' or 'unapproved'"
                        ),
                        "enum": ["uncategorized", "unapproved"],
                    },
                },
                "required": ["budget_id"],
            },
        ),
        Tool(
            name="get_transaction",
            description="Get a single transaction by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "budget_id": {
                        "type": "string",
                        "description": "The budget ID or 'last-used'",
                    },
                    "transaction_id": {
                        "type": "string",
                        "description": "The transaction ID",
                    },
                },
                "required": ["budget_id", "transaction_id"],
            },
        ),
        Tool(
            name="get_transactions_by_account",
            description="Get transactions for a specific account",
            inputSchema={
                "type": "object",
                "properties": {
                    "budget_id": {
                        "type": "string",
                        "description": "The budget ID or 'last-used'",
                    },
                    "account_id": {
                        "type": "string",
                        "description": "The account ID",
                    },
                    "since_date": {
                        "type": "string",
                        "description": (
                            "Filter transactions since this date (YYYY-MM-DD)"
                        ),
                    },
                },
                "required": ["budget_id", "account_id"],
            },
        ),
        Tool(
            name="get_transactions_by_category",
            description="Get transactions for a specific category",
            inputSchema={
                "type": "object",
                "properties": {
                    "budget_id": {
                        "type": "string",
                        "description": "The budget ID or 'last-used'",
                    },
                    "category_id": {
                        "type": "string",
                        "description": "The category ID",
                    },
                    "since_date": {
                        "type": "string",
                        "description": (
                            "Filter transactions since this date (YYYY-MM-DD)"
                        ),
                    },
                },
                "required": ["budget_id", "category_id"],
            },
        ),
        Tool(
            name="get_transactions_by_payee",
            description="Get transactions for a specific payee",
            inputSchema={
                "type": "object",
                "properties": {
                    "budget_id": {
                        "type": "string",
                        "description": "The budget ID or 'last-used'",
                    },
                    "payee_id": {
                        "type": "string",
                        "description": "The payee ID",
                    },
                    "since_date": {
                        "type": "string",
                        "description": (
                            "Filter transactions since this date (YYYY-MM-DD)"
                        ),
                    },
                },
                "required": ["budget_id", "payee_id"],
            },
        ),
        Tool(
            name="get_months",
            description="Get all budget months",
            inputSchema={
                "type": "object",
                "properties": {
                    "budget_id": {
                        "type": "string",
                        "description": "The budget ID or 'last-used'",
                    }
                },
                "required": ["budget_id"],
            },
        ),
        Tool(
            name="get_month",
            description="Get a single budget month with category balances",
            inputSchema={
                "type": "object",
                "properties": {
                    "budget_id": {
                        "type": "string",
                        "description": "The budget ID or 'last-used'",
                    },
                    "month": {
                        "type": "string",
                        "description": (
                            "The month in YYYY-MM-DD format (day will be ignored)"
                        ),
                    },
                },
                "required": ["budget_id", "month"],
            },
        ),
        Tool(
            name="get_scheduled_transactions",
            description="Get all scheduled transactions for a budget",
            inputSchema={
                "type": "object",
                "properties": {
                    "budget_id": {
                        "type": "string",
                        "description": "The budget ID or 'last-used'",
                    }
                },
                "required": ["budget_id"],
            },
        ),
        Tool(
            name="get_scheduled_transaction",
            description="Get a single scheduled transaction by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "budget_id": {
                        "type": "string",
                        "description": "The budget ID or 'last-used'",
                    },
                    "scheduled_transaction_id": {
                        "type": "string",
                        "description": "The scheduled transaction ID",
                    },
                },
                "required": ["budget_id", "scheduled_transaction_id"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""
    logger.info(f"Tool called: {name} with arguments: {arguments}")

    try:
        with get_ynab_client() as client:
            result = await _execute_tool(client, name, arguments)
            return [TextContent(type="text", text=format_response(result))]
    except YNABClientError as e:
        logger.error(f"YNAB API error: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return [TextContent(type="text", text=f"Configuration Error: {str(e)}")]
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def _execute_tool(
    client: YNABClient, name: str, arguments: dict[str, Any]
) -> dict[str, Any]:
    """Execute the specified tool and return the result."""
    match name:
        case "get_budgets":
            return client.get_budgets()
        case "get_budget":
            return client.get_budget(arguments["budget_id"])
        case "get_budget_settings":
            return client.get_budget_settings(arguments["budget_id"])
        case "get_accounts":
            return client.get_accounts(arguments["budget_id"])
        case "get_account":
            return client.get_account(arguments["budget_id"], arguments["account_id"])
        case "get_categories":
            return client.get_categories(arguments["budget_id"])
        case "get_category":
            return client.get_category(
                arguments["budget_id"], arguments["category_id"]
            )
        case "get_payees":
            return client.get_payees(arguments["budget_id"])
        case "get_payee":
            return client.get_payee(arguments["budget_id"], arguments["payee_id"])
        case "get_transactions":
            return client.get_transactions(
                arguments["budget_id"],
                since_date=arguments.get("since_date"),
                type_filter=arguments.get("type"),
            )
        case "get_transaction":
            return client.get_transaction(
                arguments["budget_id"], arguments["transaction_id"]
            )
        case "get_transactions_by_account":
            return client.get_transactions_by_account(
                arguments["budget_id"],
                arguments["account_id"],
                since_date=arguments.get("since_date"),
            )
        case "get_transactions_by_category":
            return client.get_transactions_by_category(
                arguments["budget_id"],
                arguments["category_id"],
                since_date=arguments.get("since_date"),
            )
        case "get_transactions_by_payee":
            return client.get_transactions_by_payee(
                arguments["budget_id"],
                arguments["payee_id"],
                since_date=arguments.get("since_date"),
            )
        case "get_months":
            return client.get_months(arguments["budget_id"])
        case "get_month":
            return client.get_month(arguments["budget_id"], arguments["month"])
        case "get_scheduled_transactions":
            return client.get_scheduled_transactions(arguments["budget_id"])
        case "get_scheduled_transaction":
            return client.get_scheduled_transaction(
                arguments["budget_id"], arguments["scheduled_transaction_id"]
            )
        case _:
            raise ValueError(f"Unknown tool: {name}")


async def main() -> None:
    """Main entry point for the MCP server."""
    logger.info("Starting YNAB MCP Server")

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
