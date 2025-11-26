# YNAB MCP Server

A containerized MCP (Model Context Protocol) server in Python that integrates with the YNAB API using a personal access token for read-only operations.

## Overview

This server provides read-only access to your YNAB (You Need A Budget) data through the Model Context Protocol (MCP). It allows AI assistants and other MCP clients to query your budget information, accounts, transactions, and more.

## Features

- **Read-only access** to YNAB budgets, accounts, categories, payees, and transactions
- **Scheduled transactions** support for viewing recurring transactions
- **Monthly budget** data with category balances
- **Containerized** for easy deployment
- **VS Code DevContainer** for seamless development
- **Comprehensive test suite** with pytest
- **Type hints** throughout the codebase

## Prerequisites

- Python 3.10 or higher
- Docker (optional, for containerized deployment)
- VS Code with Remote Containers extension (optional, for development)
- YNAB Personal Access Token ([Get one here](https://app.ynab.com/settings/developer))

## Installation

### From Source

1. Clone the repository:

   ```bash
   git clone https://github.com/brynsp/mcp-ynab.git
   cd mcp-ynab
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set your YNAB personal access token:

   ```bash
   export YNAB_TOKEN=your-personal-access-token
   ```

### Using Docker

1. Build the Docker image:

   ```bash
   docker build -t ynab-mcp-server .
   ```

2. Run the container:

   ```bash
   docker run -e YNAB_TOKEN=your-personal-access-token ynab-mcp-server
   ```

## Running the Server

### Locally

```bash
export YNAB_TOKEN=your-personal-access-token
python -m src.main
```

### In Docker

```bash
docker run -e YNAB_TOKEN=your-personal-access-token ynab-mcp-server
```

## Configuration

The server uses environment variables for configuration:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `YNAB_TOKEN` | Yes | - | Your YNAB personal access token |
| `YNAB_BASE_URL` | No | `https://api.ynab.com/v1` | YNAB API base URL |

## Available Tools

The MCP server exposes the following tools:

### Budget Tools

- `get_budgets` - Get all budgets
- `get_budget` - Get a single budget by ID
- `get_budget_settings` - Get budget settings

### Account Tools

- `get_accounts` - Get all accounts for a budget
- `get_account` - Get a single account by ID

### Category Tools

- `get_categories` - Get all categories for a budget
- `get_category` - Get a single category by ID

### Payee Tools

- `get_payees` - Get all payees for a budget
- `get_payee` - Get a single payee by ID

### Transaction Tools

- `get_transactions` - Get transactions (with optional filters)
- `get_transaction` - Get a single transaction by ID
- `get_transactions_by_account` - Get transactions for a specific account
- `get_transactions_by_category` - Get transactions for a specific category
- `get_transactions_by_payee` - Get transactions for a specific payee

### Monthly Budget Tools

- `get_months` - Get all budget months
- `get_month` - Get a single budget month with category balances

### Scheduled Transaction Tools

- `get_scheduled_transactions` - Get all scheduled transactions
- `get_scheduled_transaction` - Get a single scheduled transaction

## Development

### Using VS Code DevContainer

1. Open the repository in VS Code
2. Click "Reopen in Container" when prompted, or use the command palette (`Ctrl+Shift+P`) and select "Dev Containers: Reopen in Container"
3. The development environment will be set up automatically

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_ynab_client.py
```

### Linting and Type Checking

```bash
# Run ruff linter
ruff check src/ tests/

# Run ruff formatter
ruff format src/ tests/

# Run mypy type checker
mypy src/
```

## Project Structure

```text
mcp-ynab/
├── src/
│   ├── __init__.py       # Package initialization
│   ├── main.py           # MCP server entry point
│   ├── ynab_client.py    # YNAB API client
│   └── config.py         # Configuration management
├── tests/
│   ├── __init__.py
│   ├── test_main.py      # MCP server tests
│   ├── test_ynab_client.py   # YNAB client tests
│   └── test_config.py    # Configuration tests
├── docs/
│   └── README.md         # Additional documentation
├── .devcontainer/
│   ├── devcontainer.json # VS Code DevContainer config
│   └── Dockerfile        # Development container
├── Dockerfile            # Production container
├── requirements.txt      # Python dependencies
├── pyproject.toml        # Python project configuration
└── README.md             # This file
```

## API Reference

### YNAB API Documentation

For more information about the YNAB API, visit:

- [YNAB API Documentation](https://api.ynab.com/)
- [YNAB API Rate Limiting](https://api.ynab.com/#rate-limiting)

### MCP Protocol

For more information about the Model Context Protocol, visit:

- [MCP Documentation](https://modelcontextprotocol.io/)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [YNAB](https://www.ynab.com/) for providing the budgeting API
- [Model Context Protocol](https://modelcontextprotocol.io/) for the protocol specification
