# MCP API Bridge Lite

Free, minimal REST API wrapper as an MCP server. Let your AI agent call any API in 30 seconds.

## Quick Start

```bash
pip install mcp aiohttp
export MCP_API_BASE_URL=https://jsonplaceholder.typicode.com
export MCP_API_AUTH_KEY=your-key-here  # optional
python server.py
```

## Claude Desktop Configuration

```json
{
  "mcpServers": {
    "my-api": {
      "command": "python",
      "args": ["server.py"],
      "env": {
        "MCP_API_BASE_URL": "https://api.example.com",
        "MCP_API_AUTH_KEY": "your-api-key"
      }
    }
  }
}
```

## Tools

| Tool | Description |
|------|-------------|
| `api_request` | Make GET/POST/PUT/DELETE requests to any API path |

## Need More?

The **full MCP API Bridge** includes:

- JSON config file for multi-endpoint setup (no code changes needed)
- Per-minute and per-hour rate limiting
- Response caching with configurable TTL
- Auto-retry with exponential backoff
- Multiple auth types (API key, Bearer, Basic, custom headers)
- Dynamic tools generated from your endpoint config
- Concurrent request control

**[Get the full version →](https://whop.com/checkout/plan_bys1zVJEPhQji)**

## Part of the MCP Starter Arsenal

4 production-ready MCP servers: Database, API Bridge, RAG, and Web Scraper.

**[Get the full arsenal →](https://whop.com/checkout/plan_rdUWYjU5aDoA0)**
