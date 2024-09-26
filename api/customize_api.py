from functools import wraps
import logging
import api.system.api_utils as api_utils
import contextlib
import yaml
from pathlib import Path
from flask_cors import cross_origin
import safrs
from flask import request, jsonify
from flask_jwt_extended import get_jwt, jwt_required, verify_jwt_in_request
from safrs import jsonapi_rpc
from database import models
import json
import sys
from sqlalchemy import text, select, update, insert, delete
from sqlalchemy.orm import load_only
import sqlalchemy
import requests
from datetime import date
from config.config import Args
import os
from pathlib import Path
from api.system.expression_parser import parsePayload
from api.system.gen_pdf_report import gen_report

# called by api_logic_server_run.py, to customize api (new end points, services).
# separate from expose_api_models.py, to simplify merge if project recreated

app_logger = logging.getLogger(__name__)

db = safrs.DB
session = db.session
_project_dir = None


class DotDict(dict):
    """dot.notation access to dictionary attributes"""

    # thanks: https://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary/28463329
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def expose_services(app, api, project_dir, swagger_host: str, PORT: str):
    # sourcery skip: avoid-builtin-shadow
    """Customize API - new end points for services

    Brief background: see readme_customize_api.md

    """
    
    _project_dir = project_dir
    app_logger.debug("api/customize_api.py - expose custom services")

    from api.api_discovery.auto_discovery import discover_services
    discover_services(app, api, project_dir, swagger_host, PORT)
    
    @app.route("/hello_world")
    def hello_world():  # test it with: http://localhost::5656/hello_world?user=ApiLogicServer
        """
        This is inserted to illustrate that APIs not limited to database objects, but are extensible.

        See: https://apilogicserver.github.io/Docs/API-Customize/

        See: https://github.com/thomaxxl/safrs/wiki/Customization
        """

    def admin_required():
        """
        Support option to bypass security (see cats, below).

        See: https://flask-jwt-extended.readthedocs.io/en/stable/custom_decorators/
        """

        def wrapper(fn):
            @wraps(fn)
            def decorator(*args, **kwargs):
                if Args.security_enabled == False:
                    return fn(*args, **kwargs)
                verify_jwt_in_request(True)  # must be issued if security enabled
                # clientId = jwt[1].get('clientId', -1)
                return fn(*args, **kwargs)

            return decorator

        return wrapper
        user = request.args.get("user")
        return jsonify({"result": f"hello, {user}"})
