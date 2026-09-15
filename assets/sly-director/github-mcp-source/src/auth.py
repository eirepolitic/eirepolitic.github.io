import asyncio

import jwt
from jwt import PyJWKClient
from mcp.server.auth.provider import AccessToken, TokenVerifier

from .settings import AUTHKIT_ISSUER, AUTHKIT_JWKS_URL, PUBLIC_MCP_URL


_jwks_client = PyJWKClient(AUTHKIT_JWKS_URL, cache_keys=True)


class AuthKitTokenVerifier(TokenVerifier):
    """Validate WorkOS AuthKit access tokens presented to the MCP server."""

    async def verify_token(self, token: str) -> AccessToken | None:
        try:
            signing_key = await asyncio.to_thread(_jwks_client.get_signing_key_from_jwt, token)
            claims = await asyncio.to_thread(
                jwt.decode,
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=PUBLIC_MCP_URL,
                issuer=AUTHKIT_ISSUER,
                options={"require": ["exp", "iss", "sub", "aud"]},
            )
        except Exception:
            return None

        scopes = str(claims.get("scope", "")).split()
        if "openid" not in scopes:
            scopes.append("openid")

        client_id = str(claims.get("client_id") or claims.get("azp") or "authkit-mcp-client")

        return AccessToken(
            token=token,
            client_id=client_id,
            scopes=scopes,
            expires_at=int(claims["exp"]),
            resource=PUBLIC_MCP_URL,
            subject=str(claims["sub"]),
            claims=claims,
        )


# Compatibility alias while app.py is kept otherwise unchanged.
CognitoTokenVerifier = AuthKitTokenVerifier
