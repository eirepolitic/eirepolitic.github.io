import os
from urllib.parse import urlparse


def required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


GITHUB_OWNER = required("GITHUB_OWNER")
GITHUB_TOKEN = required("GITHUB_TOKEN")
COGNITO_REGION = required("COGNITO_REGION")
COGNITO_USER_POOL_ID = required("COGNITO_USER_POOL_ID")
COGNITO_APP_CLIENT_ID = required("COGNITO_APP_CLIENT_ID")
PUBLIC_MCP_URL = required("PUBLIC_MCP_URL").rstrip("/")
DEFAULT_BASE_BRANCH = os.environ.get("DEFAULT_BASE_BRANCH", "main").strip() or "main"
BRANCH_PREFIX = os.environ.get("BRANCH_PREFIX", "sly/").strip()

PUBLIC_MCP_HOST = urlparse(PUBLIC_MCP_URL).netloc
if not PUBLIC_MCP_HOST:
    raise RuntimeError("PUBLIC_MCP_URL must be a complete https:// URL")

COGNITO_ISSUER = (
    f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}"
)
COGNITO_JWKS_URL = f"{COGNITO_ISSUER}/.well-known/jwks.json"
