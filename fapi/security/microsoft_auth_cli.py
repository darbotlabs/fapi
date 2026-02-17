import json
import subprocess
from typing import Optional, Union

from annotated_doc import Doc
from fapi.exceptions import HTTPException
from fapi.openapi.models import HTTPBearer as HTTPBearerModel
from fapi.security.base import SecurityBase
from fapi.security.utils import get_authorization_scheme_param
from pydantic import BaseModel
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from typing_extensions import Annotated


class MicrosoftAuthToken(BaseModel):
    """
    The Microsoft Authentication CLI token result containing user information
    and the access token.

    This is returned when using `MicrosoftAuthCLI` in a dependency.
    """

    user: Annotated[str, Doc("The authenticated user's email address.")]
    display_name: Annotated[str, Doc("The authenticated user's display name.")]
    token: Annotated[str, Doc("The access token.")]
    expiration_date: Annotated[str, Doc("The token expiration date in Unix format.")]


class MicrosoftAuthCLI(SecurityBase):
    """
    Microsoft Authentication CLI (AzureAuth) integration for Azure AD authentication.

    This security scheme integrates with the microsoft-authentication-cli tool to provide
    Azure AD authentication for FAPI applications. It supports domain filtering for both
    top-level domains (TLD) and second-level domains.

    The authentication is performed by shelling out to the `azureauth` CLI command,
    which handles all the authentication flows (IWA, WAM, Web Browser, Device Code).

    ## Usage

    Create an instance object and use that object as the dependency in `Depends()`.

    The dependency result will be a `MicrosoftAuthToken` object containing the user
    information and access token, or the raw token string if `return_token_only` is True.

    ## Example

    ```python
    from typing import Annotated

    from fastapi import Depends, FastAPI
    from fapi.security import MicrosoftAuthCLI, MicrosoftAuthToken

    app = FastAPI()

    # Using a config file with alias
    security = MicrosoftAuthCLI(
        config_path="/path/to/config.toml",
        alias="myapp"
    )

    @app.get("/users/me")
    def read_current_user(token: Annotated[MicrosoftAuthToken, Depends(security)]):
        return {"user": token.user, "display_name": token.display_name}

    # Using explicit parameters
    security_explicit = MicrosoftAuthCLI(
        client_id="73e5793e-8f71-4da2-9f71-575cb3019b37",
        resource_id="67eeda51-3891-4101-a0e3-bf0c64047157",
        tenant_id="a3be859b-7f9a-4955-98ed-f3602dbd954c",
        domain="contoso.com"
    )

    @app.get("/items")
    def read_items(token: Annotated[MicrosoftAuthToken, Depends(security_explicit)]):
        return {"token": token.token}
    ```

    ## Requirements

    This requires the `azureauth` CLI tool to be installed and available in the system PATH.
    See https://github.com/AzureAD/microsoft-authentication-cli for installation instructions.
    """

    def __init__(
        self,
        *,
        client_id: Annotated[
            Optional[str],
            Doc(
                """
                The Azure AD application (client) ID.

                This is a unique identifier assigned to your app by Azure AD when
                the app was registered. Required if not using config_path/alias.
                """
            ),
        ] = None,
        resource_id: Annotated[
            Optional[str],
            Doc(
                """
                The Azure AD resource ID.

                This is the unique ID representing the resource which you want to
                authenticate to. Required if not using config_path/alias.
                """
            ),
        ] = None,
        tenant_id: Annotated[
            Optional[str],
            Doc(
                """
                The Azure AD tenant ID.

                This identifies the Azure AD tenant for authentication.
                Required if not using config_path/alias.
                """
            ),
        ] = None,
        domain: Annotated[
            Optional[str],
            Doc(
                """
                The domain filter for user accounts.

                Supports both top-level domains (TLD) like "com" or "org",
                and second-level domains like "contoso.com" or "fabrikam.com".
                This filters which user accounts can be used for authentication.
                """
            ),
        ] = None,
        config_path: Annotated[
            Optional[str],
            Doc(
                """
                Path to the AzureAuth config file (TOML format).

                If provided along with an alias, client_id, resource_id, tenant_id,
                and domain can be read from the config file.
                """
            ),
        ] = None,
        alias: Annotated[
            Optional[str],
            Doc(
                """
                The alias name in the config file.

                Used in combination with config_path to load authentication parameters
                from a TOML configuration file.
                """
            ),
        ] = None,
        timeout: Annotated[
            Optional[float],
            Doc(
                """
                Authentication timeout in minutes.

                The default is 15 minutes. This can be overridden with a custom
                timeout value interpreted as a decimal number of minutes.
                """
            ),
        ] = None,
        azureauth_path: Annotated[
            str,
            Doc(
                """
                Path to the azureauth CLI executable.

                Defaults to "azureauth" which assumes it's in the system PATH.
                Can be overridden to specify an explicit path.
                """
            ),
        ] = "azureauth",
        scheme_name: Annotated[
            Optional[str],
            Doc(
                """
                Security scheme name.

                It will be included in the generated OpenAPI (e.g. visible at `/docs`).
                """
            ),
        ] = None,
        description: Annotated[
            Optional[str],
            Doc(
                """
                Security scheme description.

                It will be included in the generated OpenAPI (e.g. visible at `/docs`).
                """
            ),
        ] = None,
        auto_error: Annotated[
            bool,
            Doc(
                """
                By default, if the HTTP Bearer token is not provided or authentication
                fails, `MicrosoftAuthCLI` will automatically cancel the request and
                send the client an error.

                If `auto_error` is set to `False`, when authentication fails,
                instead of erroring out, the dependency result will be `None`.

                This is useful when you want to have optional authentication.
                """
            ),
        ] = True,
        return_token_only: Annotated[
            bool,
            Doc(
                """
                If True, returns only the token string instead of the full
                MicrosoftAuthToken object.

                This is useful when you only need the token and not the user
                information.
                """
            ),
        ] = False,
        verify_bearer_scheme: Annotated[
            bool,
            Doc(
                """
                If True, verifies that the Authorization header uses the Bearer scheme.

                When False, accepts any authorization header format. This is useful
                when integrating with systems that might send tokens differently.
                """
            ),
        ] = True,
    ):
        # Validate that either explicit params or config/alias are provided
        has_explicit = client_id and resource_id and tenant_id
        has_config = config_path and alias

        if not has_explicit and not has_config:
            raise ValueError(
                "Either provide (client_id, resource_id, tenant_id) "
                "or (config_path, alias)"
            )

        # Validate timeout is positive
        if timeout is not None and timeout <= 0:
            raise ValueError("timeout must be a positive number")

        self.client_id = client_id
        self.resource_id = resource_id
        self.tenant_id = tenant_id
        self.domain = domain
        self.config_path = config_path
        self.alias = alias
        self.timeout = timeout
        self.azureauth_path = azureauth_path
        self.auto_error = auto_error
        self.return_token_only = return_token_only
        self.verify_bearer_scheme = verify_bearer_scheme

        # Setup OpenAPI model
        self.model = HTTPBearerModel(
            bearerFormat="JWT", description=description or "Azure AD Bearer token"
        )
        self.scheme_name = scheme_name or self.__class__.__name__

    def _get_token_from_azureauth(self) -> Optional[MicrosoftAuthToken]:
        """
        Execute azureauth CLI to get a token.

        Returns the token information or None if authentication fails.
        """
        cmd = [self.azureauth_path, "aad"]

        # Add config/alias or explicit parameters
        if self.config_path and self.alias:
            cmd.extend(["--config", self.config_path, "--alias", self.alias])
        else:
            if self.client_id:
                cmd.extend(["--client", self.client_id])
            if self.resource_id:
                cmd.extend(["--resource", self.resource_id])
            if self.tenant_id:
                cmd.extend(["--tenant", self.tenant_id])

        # Add optional parameters
        if self.domain:
            cmd.extend(["--domain", self.domain])
        if self.timeout:
            cmd.extend(["--timeout", str(self.timeout)])

        # Request JSON output
        cmd.extend(["--output", "json"])

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=self.timeout * 60 if self.timeout else 900,  # Default 15 min
            )

            # Parse JSON response
            token_data = json.loads(result.stdout)
            return MicrosoftAuthToken(**token_data)

        except subprocess.CalledProcessError:
            return None
        except subprocess.TimeoutExpired:
            return None
        except (json.JSONDecodeError, ValueError):
            return None
        except FileNotFoundError:
            # azureauth not found in PATH
            return None

    async def __call__(
        self, request: Request
    ) -> Union[MicrosoftAuthToken, str, None]:
        """
        Validate the authorization header and authenticate using azureauth CLI.

        Returns:
            - MicrosoftAuthToken object if return_token_only is False
            - Token string if return_token_only is True
            - None if auto_error is False and authentication fails
        """
        authorization = request.headers.get("Authorization")

        if self.verify_bearer_scheme:
            scheme, credentials = get_authorization_scheme_param(authorization)
            if not (authorization and scheme and credentials):
                if self.auto_error:
                    raise HTTPException(
                        status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
                    )
                else:
                    return None

            if scheme.lower() != "bearer":
                if self.auto_error:
                    raise HTTPException(
                        status_code=HTTP_401_UNAUTHORIZED,
                        detail="Invalid authentication credentials",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                else:
                    return None

        # Get token from azureauth
        token_info = self._get_token_from_azureauth()

        if token_info is None:
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None

        # Return token only or full object
        if self.return_token_only:
            return token_info.token
        return token_info
