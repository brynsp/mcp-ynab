# YNAB MCP Server Documentation

## Architecture

The YNAB MCP Server is designed with modularity and extensibility in mind. Here's an overview of the architecture:

### Components

1. **Configuration Module (`config.py`)**
   - Handles environment variable management
   - Provides a centralized configuration object
   - Validates required configuration at startup

2. **YNAB Client (`ynab_client.py`)**
   - Wraps the YNAB API using httpx
   - Provides type-safe methods for all read-only endpoints
   - Handles error translation and HTTP details

3. **MCP Server (`main.py`)**
   - Implements the MCP protocol using the mcp library
   - Exposes YNAB operations as MCP tools
   - Handles request/response formatting

### Data Flow

```
MCP Client -> MCP Server (main.py) -> YNAB Client (ynab_client.py) -> YNAB API
```

## Extending the Server

### Adding New Tools

To add a new tool:

1. Add the YNAB API method to `ynab_client.py`:
   ```python
   def get_new_data(self, budget_id: str) -> dict[str, Any]:
       """Get new data from YNAB."""
       return self._make_request(f"/budgets/{budget_id}/new-endpoint")
   ```

2. Add the tool definition to `list_tools()` in `main.py`:
   ```python
   Tool(
       name="get_new_data",
       description="Get new data from YNAB",
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
   ```

3. Add the tool handler to `_execute_tool()`:
   ```python
   case "get_new_data":
       return client.get_new_data(arguments["budget_id"])
   ```

4. Add tests for the new functionality.

### Adding Write Operations

While this server is designed for read-only access, you can extend it for write operations:

1. Add POST/PUT/PATCH methods to `YNABClient`
2. Create new tools with appropriate input schemas
3. Update the tool handler to call the new methods

**Note:** Be careful with write operations and consider adding confirmation prompts.

## Troubleshooting

### Common Issues

1. **"YNAB_TOKEN environment variable is required"**
   - Ensure you've set the `YNAB_TOKEN` environment variable
   - Check that the token is valid and not expired

2. **"YNAB API request failed with status 401"**
   - Your token may be invalid or expired
   - Generate a new token from the YNAB developer settings

3. **"YNAB API request failed with status 429"**
   - You've exceeded the YNAB API rate limit
   - Wait a few seconds before making more requests

### Debug Logging

Enable debug logging by setting the log level:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Security Considerations

1. **Token Security**
   - Never commit your YNAB token to version control
   - Use environment variables or secrets management
   - Consider using a `.env` file locally (not committed)

2. **Container Security**
   - The container runs as a non-root user
   - Only necessary dependencies are installed
   - No shell access in the production container

3. **API Access**
   - This server only provides read-only access
   - No modifications to your YNAB data are possible through this server
