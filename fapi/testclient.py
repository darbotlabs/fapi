"""
FastAPI TestClient for testing applications without actual HTTP/socket connections.

The TestClient allows you to test FastAPI applications by communicating directly
with the FastAPI code, without creating actual HTTP and socket connections.
"""

from starlette.testclient import TestClient as StarletteTestClient


class TestClient(StarletteTestClient):
    """
    Test client for FastAPI applications.

    This client allows you to make requests to your FastAPI application without
    running an actual HTTP server. It's based on Starlette's TestClient and uses
    the HTTPX library under the hood.

    Example:
        ```python
        from fastapi import FastAPI
        from fapi.testclient import TestClient

        app = FastAPI()

        @app.get("/")
        def read_root():
            return {"Hello": "World"}

        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"Hello": "World"}
        ```

    For more information about testing FastAPI applications, see the
    [Testing documentation](https://fastapi.tiangolo.com/tutorial/testing/).

    For authentication testing, see the
    [Security documentation](https://fastapi.tiangolo.com/tutorial/security/).

    Args:
        app: The FastAPI application to test
        base_url: Base URL for the test client (default: "http://testserver")
        raise_server_exceptions: Whether to raise exceptions that occur in the
            application (default: True)
        root_path: The root path of the application (default: "")
        backend: The async backend to use (default: "asyncio")
        backend_options: Options for the async backend
        cookies: Initial cookies to include with requests
        headers: Default headers to include with all requests
        follow_redirects: Whether to automatically follow redirects (default: True)
    """

    pass


__all__ = ["TestClient"]
