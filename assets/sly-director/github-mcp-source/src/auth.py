import asyncio

import jwt
from jwt import PyJWKClient
from mcp.server.auth.provider import AccessToken, TokenVerifier

from .settings import (
    COGNITO_APP_CLIENT_ID,
    COGNITO_ISSUER,
    COGNITO_JWKS_URL,
    PUBLIC_MCP_URL,
)


_jwks_client = PyJWKClient(COGNITO_JWKS_URL, cache_keys=True)


class CognitoTokenVerifier(TokenVerifier):
    """Validate Cognito access tokens presented to the MCP server."""

    async def verify_token(self, token: str) -> AccessToken | None:
        try:
            signing_key = await asyncio.to_thread(_jwks_client.get_signing_key_from_jwt, token)
            claims = await asyncio.to_thread(
                jwt.decode,
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=PUBLIC_MCP_URL,
                issuer=COGNITO_ISSUER,
                options={
                    "require": ["exp", "iss", "sub", "client_id", "token_use", "aud"],
                },
            )
        except Exception:
            return None

        if claims.get("token_use") != "access":
            return None
        if claims.get("client_id") != COGNITO_APP_CLIENT_ID:
            return None

        scopes = str(claims.get("scope", "")).split()
        if "openid" not in scopes:
            return None

        return AccessToken(
            token=token,
            client_id=str(claims["client_id"]),
            scopes=scopes,
            expires_at=int(claims["exp"]),
            resource=PUBLIC_MCP_URL,
            subject=str(claims["sub"]),
            claims=claims,
        )
