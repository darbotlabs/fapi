"""
Example usage of MicrosoftAuthCLI security scheme.

This example demonstrates how to use the Microsoft Authentication CLI integration
in FAPI to authenticate users with Azure AD.

Requirements:
- azureauth CLI tool installed (https://github.com/AzureAD/microsoft-authentication-cli)
- Azure AD application registration with appropriate configuration
"""

from datetime import datetime
from typing import Annotated

from fapi import Depends, FastAPI
from fapi.security import MicrosoftAuthCLI, MicrosoftAuthToken

app = FastAPI(
    title="Microsoft Auth CLI Example",
    description="Example of using Microsoft Authentication CLI for Azure AD authentication",
)

# Example 1: Using explicit parameters with TLD domain filter
security_tld = MicrosoftAuthCLI(
    client_id="your-client-id",
    resource_id="your-resource-id",
    tenant_id="your-tenant-id",
    domain="com",  # TLD filter - only allows users from .com domains
    description="Azure AD authentication with TLD filter",
)


# Example 2: Using second-level domain filter
security_second_level = MicrosoftAuthCLI(
    client_id="your-client-id",
    resource_id="your-resource-id",
    tenant_id="your-tenant-id",
    domain="contoso.com",  # Second-level domain filter
    description="Azure AD authentication with domain filter",
)


# Example 3: Using config file and alias
security_config = MicrosoftAuthCLI(
    config_path="/path/to/config.toml",
    alias="myapp",
    description="Azure AD authentication using config file",
)


# Example 4: Optional authentication with auto_error=False
security_optional = MicrosoftAuthCLI(
    client_id="your-client-id",
    resource_id="your-resource-id",
    tenant_id="your-tenant-id",
    auto_error=False,
    description="Optional Azure AD authentication",
)


@app.get("/")
def root() -> dict:
    """Public endpoint that doesn't require authentication."""
    return {
        "message": "Welcome to the Microsoft Auth CLI example",
        "endpoints": {
            "/users/me": "Get current user info (TLD filter)",
            "/users/profile": "Get user profile (domain filter)",
            "/config/user": "Get user via config (config-based auth)",
            "/optional": "Optional authentication endpoint",
        },
    }


@app.get("/users/me")
def get_current_user(
    token: Annotated[MicrosoftAuthToken, Depends(security_tld)],
) -> dict:
    """
    Get the current authenticated user information.

    Uses TLD domain filter (only .com domains allowed).
    Requires Bearer token in Authorization header.
    """
    return {
        "user": token.user,
        "display_name": token.display_name,
        "token_expiration": token.expiration_date,
    }


@app.get("/users/profile")
def get_user_profile(
    token: Annotated[MicrosoftAuthToken, Depends(security_second_level)],
) -> dict:
    """
    Get user profile information.

    Uses second-level domain filter (only contoso.com allowed).
    Requires Bearer token in Authorization header.
    """
    return {
        "user": token.user,
        "display_name": token.display_name,
        "domain": token.user.split("@")[1] if "@" in token.user else "unknown",
    }


@app.get("/config/user")
def get_user_from_config(
    token: Annotated[MicrosoftAuthToken, Depends(security_config)],
) -> dict:
    """
    Get user information using config-based authentication.

    Uses configuration file and alias for authentication parameters.
    Requires Bearer token in Authorization header.
    """
    return {
        "authenticated": True,
        "user": token.user,
        "display_name": token.display_name,
    }


@app.get("/optional")
def optional_auth(
    token: Annotated[MicrosoftAuthToken | None, Depends(security_optional)],
) -> dict:
    """
    Endpoint with optional authentication.

    Returns different information based on whether user is authenticated.
    """
    if token is None:
        return {
            "authenticated": False,
            "message": "No authentication provided",
        }

    return {
        "authenticated": True,
        "user": token.user,
        "display_name": token.display_name,
    }


@app.get("/protected/data")
def get_protected_data(
    token: Annotated[MicrosoftAuthToken, Depends(security_tld)],
) -> dict:
    """
    Get protected data that requires authentication.

    This endpoint requires valid Azure AD authentication.
    """
    return {
        "data": "This is protected data",
        "accessed_by": token.user,
        "access_time": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    import uvicorn

    # Note: This is for demonstration purposes only
    # In production, you would need to:
    # 1. Install azureauth CLI tool
    # 2. Configure your Azure AD application
    # 3. Update the client_id, resource_id, and tenant_id values
    # 4. Set up the config file if using config-based authentication

    print("Starting Microsoft Auth CLI example server...")
    print("Make sure you have azureauth CLI tool installed!")
    print("Visit http://localhost:8043/docs for API documentation")

    uvicorn.run(app, host="0.0.0.0", port=8043)
