import os
from urllib.parse import urlparse


def required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def normalized_https_url(name: str) -> str:
    value = required(name).rstrip("/")
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.netloc:
        raise RuntimeError(f"{name} must be a complete https:// URL")
    return value


GITHUB_OWNER = required("GITHUB_OWNER")
GITHUB_TOKEN = required("GITHUB_TOKEN")
PUBLIC_MCP_URL = normalized_https_url("PUBLIC_MCP_URL")
AUTHKIT_ISSUER = normalized_https_url("AUTHKIT_ISSUER")
DEFAULT_BASE_BRANCH = os.environ.get("DEFAULT_BASE_BRANCH", "main").strip() or "main"
BRANCH_PREFIX = os.environ.get("BRANCH_PREFIX", "sly/").strip()

PUBLIC_MCP_HOST = urlparse(PUBLIC_MCP_URL).netloc
AUTHKIT_JWKS_URL = f"{AUTHKIT_ISSUER}/oauth2/jwks"
AUTHKIT_METADATA_URL = f"{AUTHKIT_ISSUER}/.well-known/oauth-authorization-server"
