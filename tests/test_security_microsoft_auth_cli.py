from typing import Optional
from unittest.mock import MagicMock, patch

import pytest
from fapi import FastAPI, Security
from fapi.security import MicrosoftAuthCLI, MicrosoftAuthToken
from fapi.testclient import TestClient


def test_microsoft_auth_cli_with_explicit_params():
    """Test MicrosoftAuthCLI with explicit client_id, resource_id, tenant_id."""
    app = FastAPI()

    security = MicrosoftAuthCLI(
        client_id="test-client-id",
        resource_id="test-resource-id",
        tenant_id="test-tenant-id",
        domain="contoso.com",
        auto_error=True,
    )

    @app.get("/users/me")
    async def read_current_user(
        token: MicrosoftAuthToken = Security(security),
    ) -> dict:
        return {
            "user": token.user,
            "display_name": token.display_name,
            "token": token.token,
        }

    client = TestClient(app)

    # Mock the subprocess call to azureauth
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            stdout='{"user": "test@contoso.com", "display_name": "Test User", "token": "test-token-12345", "expiration_date": "1234567890"}',
            returncode=0,
        )

        response = client.get(
            "/users/me", headers={"Authorization": "Bearer test-token"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["user"] == "test@contoso.com"
        assert data["display_name"] == "Test User"
        assert data["token"] == "test-token-12345"

        # Verify the subprocess was called with correct arguments
        mock_run.assert_called_once()
        call_args = mock_run.call_args
        cmd = call_args[0][0]
        assert "azureauth" in cmd
        assert "aad" in cmd
        assert "--client" in cmd
        assert "test-client-id" in cmd
        assert "--resource" in cmd
        assert "test-resource-id" in cmd
        assert "--tenant" in cmd
        assert "test-tenant-id" in cmd
        assert "--domain" in cmd
        assert "contoso.com" in cmd
        assert "--output" in cmd
        assert "json" in cmd


def test_microsoft_auth_cli_with_config_alias():
    """Test MicrosoftAuthCLI with config file and alias."""
    app = FastAPI()

    security = MicrosoftAuthCLI(
        config_path="/path/to/config.toml",
        alias="myapp",
        auto_error=True,
    )

    @app.get("/items")
    async def read_items(
        token: MicrosoftAuthToken = Security(security),
    ) -> dict:
        return {"token": token.token}

    client = TestClient(app)

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            stdout='{"user": "user@example.com", "display_name": "Example User", "token": "example-token", "expiration_date": "9876543210"}',
            returncode=0,
        )

        response = client.get("/items", headers={"Authorization": "Bearer test-token"})
        assert response.status_code == 200
        data = response.json()
        assert data["token"] == "example-token"

        # Verify the subprocess was called with config and alias
        mock_run.assert_called_once()
        call_args = mock_run.call_args
        cmd = call_args[0][0]
        assert "azureauth" in cmd
        assert "aad" in cmd
        assert "--config" in cmd
        assert "/path/to/config.toml" in cmd
        assert "--alias" in cmd
        assert "myapp" in cmd


def test_microsoft_auth_cli_return_token_only():
    """Test MicrosoftAuthCLI with return_token_only=True."""
    app = FastAPI()

    security = MicrosoftAuthCLI(
        client_id="test-client-id",
        resource_id="test-resource-id",
        tenant_id="test-tenant-id",
        return_token_only=True,
        auto_error=True,
    )

    @app.get("/token")
    async def get_token(token: str = Security(security)) -> dict:
        return {"token": token, "length": len(token)}

    client = TestClient(app)

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            stdout='{"user": "user@test.com", "display_name": "User", "token": "my-token", "expiration_date": "123"}',
            returncode=0,
        )

        response = client.get("/token", headers={"Authorization": "Bearer test"})
        assert response.status_code == 200
        data = response.json()
        assert data["token"] == "my-token"
        assert data["length"] == len("my-token")


def test_microsoft_auth_cli_no_authorization_header():
    """Test MicrosoftAuthCLI without authorization header."""
    app = FastAPI()

    security = MicrosoftAuthCLI(
        client_id="test-client-id",
        resource_id="test-resource-id",
        tenant_id="test-tenant-id",
        auto_error=True,
    )

    @app.get("/protected")
    async def protected_route(token: MicrosoftAuthToken = Security(security)) -> dict:
        return {"token": token.token}

    client = TestClient(app)

    response = client.get("/protected")
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authenticated"


def test_microsoft_auth_cli_invalid_bearer_scheme():
    """Test MicrosoftAuthCLI with invalid bearer scheme."""
    app = FastAPI()

    security = MicrosoftAuthCLI(
        client_id="test-client-id",
        resource_id="test-resource-id",
        tenant_id="test-tenant-id",
        auto_error=True,
    )

    @app.get("/protected")
    async def protected_route(token: MicrosoftAuthToken = Security(security)) -> dict:
        return {"token": token.token}

    client = TestClient(app)

    response = client.get("/protected", headers={"Authorization": "Basic credentials"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid authentication credentials"


def test_microsoft_auth_cli_optional_auto_error_false():
    """Test MicrosoftAuthCLI with auto_error=False."""
    app = FastAPI()

    security = MicrosoftAuthCLI(
        client_id="test-client-id",
        resource_id="test-resource-id",
        tenant_id="test-tenant-id",
        auto_error=False,
    )

    @app.get("/items")
    async def read_items(
        token: Optional[MicrosoftAuthToken] = Security(security),
    ) -> dict:
        if token is None:
            return {"msg": "No authentication provided"}
        return {"user": token.user}

    client = TestClient(app)

    # Without authorization header
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == {"msg": "No authentication provided"}

    # With authorization header but auth fails
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="Auth failed")

        response = client.get("/items", headers={"Authorization": "Bearer test"})
        assert response.status_code == 200
        assert response.json() == {"msg": "No authentication provided"}


def test_microsoft_auth_cli_with_timeout():
    """Test MicrosoftAuthCLI with custom timeout."""
    app = FastAPI()

    security = MicrosoftAuthCLI(
        client_id="test-client-id",
        resource_id="test-resource-id",
        tenant_id="test-tenant-id",
        timeout=5.5,  # 5.5 minutes
        auto_error=True,
    )

    @app.get("/data")
    async def get_data(token: MicrosoftAuthToken = Security(security)) -> dict:
        return {"token": token.token}

    client = TestClient(app)

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            stdout='{"user": "u@test.com", "display_name": "U", "token": "tok", "expiration_date": "1"}',
            returncode=0,
        )

        response = client.get("/data", headers={"Authorization": "Bearer test"})
        assert response.status_code == 200

        # Check timeout was passed correctly
        call_args = mock_run.call_args
        cmd = call_args[0][0]
        assert "--timeout" in cmd
        assert "5.5" in cmd


def test_microsoft_auth_cli_tld_domain_filter():
    """Test MicrosoftAuthCLI with TLD domain filter."""
    app = FastAPI()

    security = MicrosoftAuthCLI(
        client_id="test-client-id",
        resource_id="test-resource-id",
        tenant_id="test-tenant-id",
        domain="com",  # TLD filter
        auto_error=True,
    )

    @app.get("/data")
    async def get_data(token: MicrosoftAuthToken = Security(security)) -> dict:
        return {"user": token.user}

    client = TestClient(app)

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            stdout='{"user": "test@example.com", "display_name": "Test", "token": "token", "expiration_date": "1"}',
            returncode=0,
        )

        response = client.get("/data", headers={"Authorization": "Bearer test"})
        assert response.status_code == 200

        # Verify domain filter was applied
        call_args = mock_run.call_args
        cmd = call_args[0][0]
        assert "--domain" in cmd
        assert "com" in cmd


def test_microsoft_auth_cli_second_level_domain_filter():
    """Test MicrosoftAuthCLI with second-level domain filter."""
    app = FastAPI()

    security = MicrosoftAuthCLI(
        client_id="test-client-id",
        resource_id="test-resource-id",
        tenant_id="test-tenant-id",
        domain="contoso.com",  # Second-level domain filter
        auto_error=True,
    )

    @app.get("/data")
    async def get_data(token: MicrosoftAuthToken = Security(security)) -> dict:
        return {"user": token.user}

    client = TestClient(app)

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            stdout='{"user": "admin@contoso.com", "display_name": "Admin", "token": "token", "expiration_date": "1"}',
            returncode=0,
        )

        response = client.get("/data", headers={"Authorization": "Bearer test"})
        assert response.status_code == 200
        data = response.json()
        assert data["user"] == "admin@contoso.com"

        # Verify domain filter was applied
        call_args = mock_run.call_args
        cmd = call_args[0][0]
        assert "--domain" in cmd
        assert "contoso.com" in cmd


def test_microsoft_auth_cli_verify_bearer_scheme_false():
    """Test MicrosoftAuthCLI with verify_bearer_scheme=False."""
    app = FastAPI()

    security = MicrosoftAuthCLI(
        client_id="test-client-id",
        resource_id="test-resource-id",
        tenant_id="test-tenant-id",
        verify_bearer_scheme=False,
        auto_error=True,
    )

    @app.get("/data")
    async def get_data(token: MicrosoftAuthToken = Security(security)) -> dict:
        return {"user": token.user}

    client = TestClient(app)

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            stdout='{"user": "test@test.com", "display_name": "Test", "token": "token", "expiration_date": "1"}',
            returncode=0,
        )

        # Should work even without Authorization header when verify_bearer_scheme is False
        response = client.get("/data")
        assert response.status_code == 200


def test_microsoft_auth_cli_validation_error():
    """Test MicrosoftAuthCLI raises ValueError when missing required params."""
    with pytest.raises(ValueError) as exc_info:
        MicrosoftAuthCLI()

    assert "Either provide (client_id, resource_id, tenant_id)" in str(exc_info.value)


def test_microsoft_auth_cli_openapi_schema():
    """Test that MicrosoftAuthCLI generates correct OpenAPI schema."""
    app = FastAPI()

    security = MicrosoftAuthCLI(
        client_id="test-client-id",
        resource_id="test-resource-id",
        tenant_id="test-tenant-id",
        description="Azure AD authentication",
        auto_error=True,
    )

    @app.get("/secure")
    async def secure_endpoint(token: MicrosoftAuthToken = Security(security)) -> dict:
        return {"secure": True}

    client = TestClient(app)
    response = client.get("/openapi.json")
    assert response.status_code == 200

    openapi_schema = response.json()
    assert "components" in openapi_schema
    assert "securitySchemes" in openapi_schema["components"]
    assert "MicrosoftAuthCLI" in openapi_schema["components"]["securitySchemes"]

    scheme = openapi_schema["components"]["securitySchemes"]["MicrosoftAuthCLI"]
    assert scheme["type"] == "http"
    assert scheme["scheme"] == "bearer"
    assert scheme["bearerFormat"] == "JWT"
    assert scheme["description"] == "Azure AD authentication"

    # Check that the endpoint has security requirement
    assert "paths" in openapi_schema
    assert "/secure" in openapi_schema["paths"]
    secure_path = openapi_schema["paths"]["/secure"]["get"]
    assert "security" in secure_path
    assert {"MicrosoftAuthCLI": []} in secure_path["security"]


def test_microsoft_auth_cli_custom_azureauth_path():
    """Test MicrosoftAuthCLI with custom azureauth path."""
    app = FastAPI()

    security = MicrosoftAuthCLI(
        client_id="test-client-id",
        resource_id="test-resource-id",
        tenant_id="test-tenant-id",
        azureauth_path="/custom/path/azureauth",
        auto_error=True,
    )

    @app.get("/data")
    async def get_data(token: MicrosoftAuthToken = Security(security)) -> dict:
        return {"token": token.token}

    client = TestClient(app)

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            stdout='{"user": "u@test.com", "display_name": "U", "token": "tok", "expiration_date": "1"}',
            returncode=0,
        )

        response = client.get("/data", headers={"Authorization": "Bearer test"})
        assert response.status_code == 200

        # Verify custom path was used
        call_args = mock_run.call_args
        cmd = call_args[0][0]
        assert "/custom/path/azureauth" in cmd
