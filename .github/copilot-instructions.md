# Copilot Instructions for mcp-ynab

This repository contains a Model Context Protocol (MCP) server for YNAB (You Need A Budget).

## Project Overview

- **Purpose**: Provide an MCP server that enables AI assistants to interact with YNAB's budgeting API
- **Technology**: Python MCP server implementation

## Development Guidelines

### Code Style

- Follow TypeScript best practices
- Use meaningful variable and function names
- Include JSDoc comments for public APIs
- Keep functions focused and single-purpose

### Testing

- Write tests for new functionality
- Ensure existing tests pass before submitting changes
- Test edge cases and error handling

### Security

- Never commit API keys, tokens, or secrets
- Use environment variables for sensitive configuration
- Validate all user inputs
- Follow YNAB API rate limiting guidelines

### MCP Server Development

- Follow the Model Context Protocol specification
- Implement proper error handling for tool calls
- Provide clear, descriptive tool and resource definitions
- Handle YNAB API responses appropriately

## File Structure

When adding new features:
- Place source code in the `src/` directory
- Keep tests alongside or in a dedicated `tests/` directory
- Update documentation as needed

## Pull Request Guidelines

- Keep changes focused and minimal
- Write clear commit messages
- Update the README if adding new features or changing behavior
- Ensure all CI checks pass
