"""FastAPI framework, high performance, easy to learn, fast to code, ready for production"""

__version__ = "0.121.1"

from starlette import status as status

from .applications import FastAPI as FastAPI
from .background import BackgroundTasks as BackgroundTasks
from .cli import app_cli as cli
from .config import Config as Config
from .context import current_app as current_app
from .context import g as g
from .context import request as request
from .datastructures import UploadFile as UploadFile
from .events import emit as emit
from .events import on as on
from .extensions import Extension as Extension
from .factory import create_app as create_app
from .exceptions import HTTPException as HTTPException
from .exceptions import WebSocketException as WebSocketException
from .modules import Module as Module
from .param_functions import Body as Body
from .param_functions import Cookie as Cookie
from .param_functions import Depends as Depends
from .param_functions import File as File
from .param_functions import Form as Form
from .param_functions import Header as Header
from .param_functions import Path as Path
from .param_functions import Query as Query
from .param_functions import Security as Security
from .requests import Request as Request
from .responses import Response as Response
from .routing import APIRouter as APIRouter
from .websockets import WebSocket as WebSocket
from .websockets import WebSocketDisconnect as WebSocketDisconnect
