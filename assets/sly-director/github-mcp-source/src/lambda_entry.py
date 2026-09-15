from typing import Any

from mangum import Mangum

from .app import mcp, transport_security


def build_app():
    """Create a fresh Streamable HTTP app and session manager for one Lambda invocation."""
    return mcp.streamable_http_app(
        streamable_http_path="/mcp",
        stateless_http=True,
        json_response=True,
        transport_security=transport_security,
    )


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """AWS Lambda entrypoint with a fresh single-use MCP session manager per invocation."""
    app = build_app()
    adapter = Mangum(app, lifespan="on")
    return adapter(event, context)
