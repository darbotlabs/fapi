# FAPI

[![FAPI](https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png)](https://fastapi.tiangolo.com)

*FAPI framework, high performance, easy to learn, fast to code, ready for
production*

[![Test](https://github.com/fastapi/fastapi/actions/workflows/test.yml/badge.svg?event=push&branch=master)](https://github.com/fastapi/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster)

---

**Documentation**: (to be replaced with github.io docs)
[https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)

**Source Code**:
[https://github.com/darbotlabs/fapi](https://github.com/darbotlabs/fapi)

---

FAPI is a fork and agentic continuation of FastAPI, managed by authorative intelligence agents as part of the darbot framework. 


The key features are:

* **Fast**: Very high performance, features on par with **NodeJS** and **Go** (thanks
  to Starlette and Pydantic).
  [One of the fastest Python frameworks available](#performance).
* **Fast to code**: Increase the speed to develop features by about 200% to
  300%. \*
* **Fewer bugs**: Reduce about 40% of human (developer) induced errors. \*
* **Intuitive**: Great editor support. Completion everywhere. Less time
  debugging.
* **Easy**: Designed to be easy to use and learn. Less time reading docs.
* **Short**: Minimize code duplication. Multiple features from each parameter
  declaration. Fewer bugs.
* **Robust**: Get production-ready code. With automatic interactive
  documentation.
* **Standards-based**: Based on (and fully compatible with) the open standards
  for APIs: [OpenAPI](https://github.com/OAI/OpenAPI-Specification) (previously
  known as Swagger) and [JSON Schema](https://json-schema.org/).

\* estimation based on tests on an internal development team, building
production applications.

## Complete Development Setup Guide

This section provides step-by-step instructions for setting up a complete
FAPI development environment on a new machine. These steps were tested on
Linux with Python 3.12.3.

### Prerequisites

* Python 3.8 or higher installed
* Git installed
* Terminal/shell access (bash recommended)

### Step-by-Step Installation

Follow these steps sequentially to set up your FAPI development
environment:

#### 1. Clone the Repository

```bash
# Clone the repository to your local machine
git clone https://github.com/darbotlabs/fapi.git
cd fapi
```

#### 2. Verify Python Version

```bash
# Check that Python 3.8+ is installed
python3 --version
# Expected output: Python 3.8.x or higher (tested with 3.12.3)
```

#### 3. Create Virtual Environment

```bash
# Create a new virtual environment in the project directory
python3 -m venv venv
```

#### 4. Activate Virtual Environment

```bash
# Activate the virtual environment
source venv/bin/activate

# Your prompt should now show (venv) prefix
# On Windows use: venv\Scripts\activate
```

#### 5. Upgrade pip

```bash
# Upgrade pip to the latest version
pip install --upgrade pip
```

#### 6. Install FastAPI with All Dependencies

```bash
# Install FastAPI in editable mode with all optional dependencies
# This includes uvicorn, testing tools, and all extras
pip install -e ".[all]"
```

**What gets installed:**

* FAPI core framework
* Uvicorn ASGI server with uvloop (high performance)
* Pydantic for data validation
* Starlette web framework
* Testing client (httpx)
* Template support (jinja2)
* Form parsing (python-multipart)
* Email validation (email-validator)
* JSON serializers (orjson, ujson)
* Settings management (pydantic-settings)
* Extra types (pydantic-extra-types)

#### 7. Install Development and Testing Dependencies

```bash
# Install all test requirements and development tools
pip install -r requirements-tests.txt
```

**What gets installed:**

* pytest (testing framework)
* coverage (code coverage analysis)
* mypy (static type checker)
* ruff (linter and formatter)
* Additional testing utilities (dirty-equals, inline-snapshot)
* Database testing (SQLModel, SQLAlchemy)
* Authentication testing (PyJWT, pwdlib)
* ASGI testing (anyio with trio)
* Web framework testing (Flask)
* Type stubs for better IDE support

#### 8. Create Example Application

```bash
# Create a basic FAPI application file
cat > main.py << 'EOF'
from typing import Union

from fapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "Darbot"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
EOF
```

#### 9. Start Development Server

```bash
# Start the FAPI development server with auto-reload
fapi dev main.py --port 8043

# Alternative: Use uvicorn directly
# uvicorn main:app --reload --port 8043
```

**Server Info:**

* API Server: <http://127.0.0.1:8043>
* Interactive API docs (Swagger UI): <http://127.0.0.1:8043/docs>
* Alternative API docs (ReDoc): <http://127.0.0.1:8043/redoc>
* Auto-reload is enabled by default in dev mode

#### 10. Test the API (in a new terminal)

```bash
# Activate virtual environment in new terminal
source venv/bin/activate

# Test the root endpoint
curl http://127.0.0.1:8043/
# Expected: {"Hello":"Darbot"}

# Test the items endpoint with path and query parameters
curl http://127.0.0.1:8043/items/5?q=test
# Expected: {"item_id":5,"q":"test"}
```

#### 11. Run the Test Suite

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run specific test directory
pytest tests/test_tutorial/test_first_steps/ -v

# Run with coverage report
pytest tests/ --cov=fapi --cov-report=html

# Run type checking
mypy fapi/

# Run linting
ruff check .
```

#### 12. Verify Installation

```bash
# Check installed FAPI version
python -c "import fapi; print(fapi.__version__)"

# List all installed packages
pip list

# Run a quick test to ensure everything works
pytest tests/test_tutorial/test_first_steps/ -v
# Expected: All tests pass (3 passed in ~0.2s)
```

### Common Development Commands

Once your environment is set up, use these commands for daily development:

```bash
# Always activate virtual environment first
source venv/bin/activate

# Start development server (auto-reload enabled)
fapi dev main.py --port 8043

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/path/to/test_file.py -v

# Run tests with coverage
pytest --cov=fapi --cov-report=term-missing

# Type check the codebase
mypy fapi/

# Lint and format code
ruff check .
ruff format .

# Install new dependencies
pip install package-name

# Update requirements after adding dependencies
pip freeze > requirements.txt
```

### Troubleshooting

**Port already in use:**

```bash
# Use a different port (not recommended, best to clear existing fapi service)
fastapi dev main.py --port 8044

# Or find and kill the process using port 8043
lsof -ti:8043 | xargs kill -9
```

**Import errors:**

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -e ".[all]"
pip install -r requirements-tests.txt
```

**Test failures:**

```bash
# Clear pytest cache
rm -rf .pytest_cache
pytest --cache-clear

# Run tests with full output
pytest -vv --tb=long
```

### Project Structure

```text
fapi/
├── fapi/                 # Main FAPI package source code
├── tests/                # Comprehensive test suite
├── docs/                 # Documentation (multiple languages)
├── docs_src/             # Documentation source code examples
├── scripts/              # Utility scripts
├── main.py               # Your example application (create this)
├── venv/                 # Virtual environment (created by you)
├── requirements*.txt     # Dependency specifications
├── pyproject.toml        # Project configuration and dependencies
└── README.md             # This file
```

### Next Steps

1. Visit <http://127.0.0.1:8043/docs> to explore the interactive API
   documentation
2. Read the [Tutorial - User Guide](https://fastapi.tiangolo.com/tutorial/)
   for comprehensive examples
3. Explore the `docs_src/` directory for more example code
4. Check out `tests/` to see how FAPI itself is tested
5. Modify `main.py` to build your own API

---

## Requirements

FAPI stands on the shoulders of giants:

* [Starlette](https://www.starlette.dev/) for the web parts.
* [Pydantic](https://docs.pydantic.dev/) for the data parts.

## Installation

Create and activate a
[virtual environment](https://fastapi.tiangolo.com/virtual-environments/)
and then install FAPI:

```console
$ pip install "fapi[standard]"

---> 100%
```

**Note**: Make sure you put `"fapi[standard]"` in quotes to ensure it
works in all terminals.

## Example

### Create it

Create a file `main.py` with:

```Python
from typing import Union

from fapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "Darbot"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

<details>
<summary>Or use async def...</summary>

If your code uses `async` / `await`, use `async def`:

```Python hl_lines="9  14"
from typing import Union

from fapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "Darbot"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

**Note**:

If you don't know, check the *"In a hurry?"* section about
[`async` and `await` in the docs](https://fastapi.tiangolo.com/async/#in-a-hurry).

</details>

### Run it

Run the server with:

```console
$ fapi dev main.py

 ╭────────── FAPI CLI - Development mode ───────────╮
 │                                                     │
 │  Serving at: http://127.0.0.1:8043                  │
 │                                                     │
 │  API docs: http://127.0.0.1:8043/docs               │
 │                                                     │
 │  Running in development mode, for production use:   │
 │                                                     │
 │  fapi run                                           │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯

INFO:     Will watch for changes in these directories: ['/home/user/code/awesomeapp']
INFO:     Uvicorn running on http://127.0.0.1:8043 (Press CTRL+C to quit)
INFO:     Started reloader process [2248755] using WatchFiles
INFO:     Started server process [2248757]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

<details>
<summary>About the command fapi dev main.py...</summary>

The command `fapi dev` reads your `main.py` file, detects the **FAPI**
app in it, and starts a server using [Uvicorn](https://www.uvicorn.dev).

By default, `fapi dev` will start with auto-reload enabled for local
development.

You can read more about it in the
[FastAPI CLI docs](https://fastapi.tiangolo.com/fastapi-cli/).

</details>

### Check it

Open your browser at
[http://127.0.0.1:8043/items/5?q=somequery](http://127.0.0.1:8043/items/5?q=somequery).

You will see the JSON response as:

```JSON
{"item_id": 5, "q": "somequery"}
```

You already created an API that:

* Receives HTTP requests in the *paths* `/` and `/items/{item_id}`.
* Both *paths* take `GET` operations (also known as HTTP *methods*).
* The *path* `/items/{item_id}` has a *path parameter* `item_id` that should
  be an `int`.
* The *path* `/items/{item_id}` has an optional `str` *query parameter* `q`.

### Interactive API docs

Now go to [http://127.0.0.1:8043/docs](http://127.0.0.1:8043/docs).

You will see the automatic interactive API documentation (provided by
[Swagger UI](https://github.com/swagger-api/swagger-ui)):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Alternative API docs

And now, go to [http://127.0.0.1:8043/redoc](http://127.0.0.1:8043/redoc).

You will see the alternative automatic documentation (provided by
[ReDoc](https://github.com/Rebilly/ReDoc)):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Example upgrade

Now modify the file `main.py` to receive a body from a `PUT` request.

Declare the body using standard Python types, thanks to Pydantic.

```Python hl_lines="4  9-12  25-27"
from typing import Union

from fapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

The `fapi dev` server should reload automatically.

### Interactive API docs upgrade

Now go to [http://127.0.0.1:8043/docs](http://127.0.0.1:8043/docs).

* The interactive API documentation will be automatically updated, including
  the new body:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Click on the button "Try it out", it allows you to fill the parameters and
  directly interact with the API:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* Then click on the "Execute" button, the user interface will communicate
  with your API, send the parameters, get the results and show them on the
  screen:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Alternative API docs upgrade

And now, go to [http://127.0.0.1:8043/redoc](http://127.0.0.1:8043/redoc).

* The alternative documentation will also reflect the new query parameter and
  body:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Recap

In summary, you declare **once** the types of parameters, body, etc. as
function parameters.

You do that with standard modern Python types.

You don't have to learn a new syntax, the methods or classes of a specific
library, etc.

Just standard **Python**.

For example, for an `int`:

```Python
item_id: int
```

or for a more complex `Item` model:

```Python
item: Item
```

...and with that single declaration you get:

* Editor support, including:
  * Completion.
  * Type checks.
* Validation of data:
  * Automatic and clear errors when the data is invalid.
  * Validation even for deeply nested JSON objects.
* Conversion of input data: coming from the network to Python data and types.
  Reading from:
  * JSON.
  * Path parameters.
  * Query parameters.
  * Cookies.
  * Headers.
  * Forms.
  * Files.
* Conversion of output data: converting from Python data and types to network
  data (as JSON):
  * Convert Python types (`str`, `int`, `float`, `bool`, `list`, etc).
  * `datetime` objects.
  * `UUID` objects.
  * Database models.
  * ...and many more.
* Automatic interactive API documentation, including 2 alternative user
  interfaces:
  * Swagger UI.
  * ReDoc.

---

Coming back to the previous code example, **FAPI** will:

* Validate that there is an `item_id` in the path for `GET` and `PUT`
  requests.
* Validate that the `item_id` is of type `int` for `GET` and `PUT` requests.
  * If it is not, the client will see a useful, clear error.
* Check if there is an optional query parameter named `q` (as in
  `http://127.0.0.1:8043/items/foo?q=somequery`) for `GET` requests.
  * As the `q` parameter is declared with `= None`, it is optional.
  * Without the `None` it would be required (as is the body in the case with
    `PUT`).
* For `PUT` requests to `/items/{item_id}`, read the body as JSON:
  * Check that it has a required attribute `name` that should be a `str`.
  * Check that it has a required attribute `price` that has to be a `float`.
  * Check that it has an optional attribute `is_offer`, that should be a
    `bool`, if present.
  * All this would also work for deeply nested JSON objects.
* Convert from and to JSON automatically.
* Document everything with OpenAPI, that can be used by:
  * Interactive documentation systems.
  * Automatic client code generation systems, for many languages.
* Provide 2 interactive documentation web interfaces directly.

---

We just scratched the surface, but you already get the idea of how it all works.

Try changing the line with:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...from:

```Python
        ... "item_name": item.name ...
```

...to:

```Python
        ... "item_price": item.price ...
```

...and see how your editor will auto-complete the attributes and know their types:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

For a more complete example including more features, see the
[Tutorial - User Guide](https://fastapi.tiangolo.com/tutorial/).

**Spoiler alert**: the tutorial - user guide includes:

* Declaration of **parameters** from other different places as: **headers**,
  **cookies**, **form fields** and **files**.
* How to set **validation constraints** as `maximum_length` or `regex`.
* A very powerful and easy to use **Dependency Injection** system.
* Security and authentication, including support for **OAuth2** with **JWT
  tokens** and **HTTP Basic** auth.
* More advanced (but equally easy) techniques for declaring **deeply nested
  JSON models** (thanks to Pydantic).
* **GraphQL** integration with [Strawberry](https://strawberry.rocks) and
  other libraries.
* Many extra features (thanks to Starlette) as:
  * **WebSockets**
  * extremely easy tests based on HTTPX and `pytest`
  * **CORS**
  * **Cookie Sessions**
  * ...and more.


## Dependencies

FAPI depends on Pydantic and Starlette. Those will also get forked into the darbot framework in the future, but for now they are dependencies. 

### `standard` Dependencies

When you install FAPI with `pip install "fapi[standard]"` it comes with
the `standard` group of optional dependencies:

#### Used by Pydantic

* [`email-validator`](https://github.com/JoshData/python-email-validator) -
  for email validation.

#### Used by Starlette

* [`httpx`](https://www.python-httpx.org) - Required if you want to use the
  `TestClient`.
* [`jinja2`](https://jinja.palletsprojects.com) - Required if you want to use
  the default template configuration.
* [`python-multipart`](https://github.com/Kludex/python-multipart) - Required
  if you want to support form "parsing", with `request.form()`.

#### Used by FAPI

* [`uvicorn`](https://www.uvicorn.dev) - for the server that loads and serves
  your application. This includes `uvicorn[standard]`, which includes some
  dependencies (e.g. `uvloop`) needed for high performance serving.
* `fastapi-cli[standard]` - to provide the `fastapi` command.


### Without `standard` Dependencies

If you don't want to include the `standard` optional dependencies, you can
install with `pip install fapi` instead of
`pip install "fapi[standard]"`.

### Without `fapi-cloud-cli`

If you want to install FAPI with the standard dependencies but without the
`fapi-cloud-cli`, you can install with
`pip install "fastapi[standard-no-fapi-cloud-cli]"`.

### Additional Optional Dependencies

There are some additional dependencies you might want to install.

#### Additional optional Pydantic dependencies

* [`pydantic-settings`](https://docs.pydantic.dev/latest/usage/pydantic_settings/)
  for settings management.
* [`pydantic-extra-types`](https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/)
  for extra types to be used with Pydantic.

#### Additional optional FAPI dependencies

* [`orjson`](https://github.com/ijl/orjson) - Required if you want to use
  `ORJSONResponse`.
* [`ujson`](https://github.com/esnme/ultrajson) - Required if you want to use
  `UJSONResponse`.

## License

This project is licensed under the terms of the MIT license.
