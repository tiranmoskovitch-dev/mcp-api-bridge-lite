"""
MCP API Bridge Lite — Free Single-Endpoint REST API MCP Server
For the full version with auth, rate limiting, caching, and multi-endpoint config:
→ https://whop.com/tirantech

Part of the MCP Starter Arsenal by TiranTech.
"""

import asyncio
import json
import logging
import os
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

logger = logging.getLogger(__name__)


def build_server(base_url: str = None) -> Server:
    base_url = (base_url or os.getenv("MCP_API_BASE_URL", "")).rstrip("/")
    api_key = os.getenv("MCP_API_AUTH_KEY", "")
    server = Server("mcp-api-bridge-lite")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="api_request",
                description=f"Make an HTTP request to {base_url or 'a REST API'}.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "method": {"type": "string", "enum": ["GET", "POST", "PUT", "DELETE"], "description": "HTTP method"},
                        "path": {"type": "string", "description": "API path"},
                        "params": {"type": "object", "description": "Query parameters"},
                        "body": {"type": "object", "description": "Request body for POST/PUT"},
                    },
                    "required": ["method", "path"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
        try:
            import aiohttp
        except ImportError:
            return [TextContent(type="text", text=json.dumps({"error": "Install aiohttp: pip install aiohttp"}))]

        try:
            url = f"{base_url}/{arguments['path'].lstrip('/')}"
            headers = {"Content-Type": "application/json"}
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"

            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method=arguments["method"],
                    url=url,
                    params=arguments.get("params"),
                    json=arguments.get("body"),
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as resp:
                    try:
                        data = await resp.json()
                    except Exception:
                        data = await resp.text()
                    return [TextContent(type="text", text=json.dumps({"data": data, "status": resp.status}, default=str))]
        except Exception as e:
            return [TextContent(type="text", text=json.dumps({"error": str(e)}))]

    return server


async def main():
    server = build_server()
    logger.info("MCP API Bridge Lite started")
    logger.info("For auth, rate limiting, caching & multi-endpoint → https://whop.com/tirantech")

    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
