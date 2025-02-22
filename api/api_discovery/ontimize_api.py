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
from config.config import Config
import os
from pathlib import Path
from api.system.expression_parser import parsePayload
from api.system.gen_pdf_report import gen_report
from api.system.gen_csv_report import gen_report as csv_gen_report
from api.system.gen_pdf_report import export_pdf

# from api.gen_xlsx_report import xlsx_gen_report

# This is the Ontimize Bridge API - all endpoints will be prefixed with /ontimizeweb/services/rest
# called by api_logic_server_run.py, to customize api (new end points, services).
# separate from expose_api_models.py, to simplify merge if project recreated
# version 11.x - api_logic_server_cli/prototypes/ont_app/prototype/api/api_discovery/ontimize_api.py

app_logger = logging.getLogger(__name__)

db = safrs.DB
session = db.session
_project_dir = None
app_logger.debug("api/api_discovery/ontimize_api.py - services for ontimize") 
class DotDict(dict):
    """dot.notation access to dictionary attributes"""

    # thanks: https://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary/28463329
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators = []):
    
    
    """Ontimize API - new end points for services

    Brief background: see readme_customize_api.md

    """
    global _project_dir 
    _project_dir = project_dir
    pass
    
    def admin_required():
        """
        Support option to bypass security (see cats, below).
        """

        def wrapper(fn):
            @wraps(fn)
            def decorator(*args, **kwargs):
                if Args.instance.security_enabled == False:
                    return fn(*args, **kwargs)
                verify_jwt_in_request(True)  # must be issued if security enabled
                return fn(*args, **kwargs)

            return decorator

        return wrapper

    def gen_export(request) -> any:
        payload = json.loads(request.data) if request.data != b"" else {}
        type = payload.get("type") or "csv"
        entity = payload.get("dao")
        queryParm = payload.get("queryParm") or {}
        columns = payload.get("columns") or []
        columnTitles = payload.get("columnTitles") or []
        if not entity:
            return jsonify({})
        resource = find_model(entity)
        api_clz = resource["model"]
        resources = getMetaData(api_clz.__name__)
        attributes = resources["resources"][api_clz.__name__]["attributes"]
        if type in ["csv", "CSV"]:
            return csv_gen_report(
                api_clz, request, entity, queryParm, columns, columnTitles, attributes
            )
        elif type == "pdf":
            payload["entity"] = entity
            return export_pdf(
                api_clz, request, entity, queryParm, columns, columnTitles, attributes
            )
        # elif type == "xlsx":
        #    return xlsx_gen_report(api_clz, request, entity, queryParm, columns, columnTitles, attributes)

        return jsonify(
            {
                "code": 1,
                "message": f"Unknown export type {type}",
                "data": None,
                "sqlTypes": None,
            }
        )

    def _gen_report(request) -> any:
        payload = json.loads(request.data)

        if len(payload) == 3:
            return jsonify({})

        entity = payload["entity"]
        resource = find_model(entity)
        api_clz = resource["model"]
        resources = getMetaData(api_clz.__name__)
        attributes = resources["resources"][api_clz.__name__]["attributes"]

        return gen_report(api_clz, request, _project_dir, payload, attributes)
    @app.route('/ontimizeweb/services/rest/Entity/getattributes/search', methods=["POST","OPTIONS"])
    @cross_origin()
    @admin_required()
    def getAttributes():
        filter = request.json["filter"]
        entity_name = filter["entity_name"]
        columns = ['entity_name', 'attr', 'exclude']
        resource = find_model("EntityAttr")
        api_attributes = resource["attributes"]
        api_clz = resource["model"]

        payload = "{}" if request.data == b"" else json.loads(request.data)
        expressions, filter, columns, sqltypes, offset, pagesize, orderBy, data = (
            parsePayload(api_clz, payload)
        )

        columns = ['entity_name', 'attr', 'exclude']
        pagesize = 999  # if isSearch else pagesize
        data = get_rows(
            request, api_clz, filter, orderBy, columns, pagesize, offset
        )
        return jsonify(
                    {
                    "code": 0,
                    "totalQueryRecordsNumber": 1,
                    "startRecordIndex": 1,
                    "message": f"GetAttributes for Entity --api-endpoint={entity_name}",
                    "data": data,
                }
        )
    @app.route("/ontimizeweb/services/rest/Entity/rebuild/search", methods=["POST","PUT","OPTIONS"])
    @cross_origin()
    @admin_required()
    def rebuild():
        entity = request.json["filter"]["name"]
        file_path = get_file_path(entity)
        if file_path:
            s = file_path.split("/")
            app_name = s[-1]
            print(f'$als app-build --app={app_name} --api-endpoint={entity}')
            try:
                import subprocess
                vscode_settings_path = Path(f'{_project_dir}/.vscode/settings.json')
                with open(vscode_settings_path, "r") as file:
                    settings = json.load(file)
                python_interpreter_path = settings.get("python.defaultInterpreterPath", None).replace("/bin/python","")
                print(f"Python Interpreter Path: {python_interpreter_path}")
                #venv_dir = '/Users/tylerband/dev/ApiLogicServer/ApiLogicServer-dev/build_and_test/ApiLogicServer'#TODO - move to shell
                #venv_path = os.path.join(venv_dir, 'venv', 'bin', 'activate') #Mac only
                command = f'sh {_project_dir}/rebuild_page.sh  {python_interpreter_path} {file_path} {app_name} {entity}'
                output = subprocess.run(command, cwd=file_path, shell=True, capture_output=True, text=True, check=False)
                return jsonify(
                    {
                    "code": 0,
                    "totalQueryRecordsNumber": 1,
                    "startRecordIndex": 1,
                    "message": f"Rebuild Page for --app={app_name} --api-endpoint={entity}",
                    "data": output,
                }
            )
            except subprocess.CalledProcessError as e:
                return jsonify({"error": e.output.decode('utf-8')})
    
    
    @app.route("/api/export/csv", methods=["POST", "OPTIONS"])
    @app.route("/api/export/pdf", methods=["POST", "OPTIONS"])
    @app.route("/ontimizeweb/services/rest/export/pdf", methods=["POST", "OPTIONS"])
    @app.route("/ontimizeweb/services/rest/export/csv", methods=["POST", "OPTIONS"])
    @cross_origin()
    @admin_required()
    def export():
        print(f"export {request.path}")
        # if request.method == "OPTIONS":
        #    return jsonify(success=True)
        return gen_export(request)

    @app.route("/api/dynamicjasper", methods=["POST", "OPTIONS"])
    @app.route("/ontimizeweb/services/rest/dynamicjasper", methods=["POST", "OPTIONS"])
    @cross_origin()
    @admin_required()
    def dynamicjasper():
        if request.method == "OPTIONS":
            return jsonify(success=True)
        return _gen_report(request)

    @app.route("/api/bundle", methods=["POST", "OPTIONS"])
    @app.route("/ontimizeweb/services/rest/bundle", methods=["POST", "OPTIONS"])
    @cross_origin()
    @admin_required()
    def bundle():
        if request.method == "OPTIONS":
            return jsonify(success=True)
        return jsonify({"code": 0, "data": {}, "message": None})

    @app.route("/main/YamlFiles", methods=["GET", "POST", "DELETE", "OPTIONS"])
    @cross_origin()
    @admin_required()
    @admin_required()
    def getFiles(path):
        method = request.method
        # if method == 'OPTIONS':
        #    return jsonify(success=True)
        files = session.query(models.YamlFiles).all()
        return jsonify({"code": 0, "message": "Yaml Files", "data": files})

    @app.route(
        "/ontimizeweb/services/rest/merge_rules",
        methods=["GET", "POST", "DELETE", "OPTIONS"],
    )
    @cross_origin()
    @admin_required()
    def merge_rules():
        method = request.method
        if method == "OPTIONS":
            return jsonify(success=True)
        if method == "POST":
            data = json.loads(request.data)
            path = data.get("path")
        else:
            path = "/Users/tylerband/ontimize/northwind-retool-jsonapi"
        # parse the {path}/logic/declare_logic.py file
        dir = f"{path}/logic/declare_logic.py"
        from api.api_discovery.rule_parser import insert_rules_from_file

        insert_rules_from_file(dir)

        return jsonify({"code": 0, "message": "Merge Rules", "data": {}})

    
    def insertFile(content):
        
        data = content["data"]
        if data and len(data) < 7:
            raise Exception("Invalid file content")
    
        sql_alchemy_row = models.YamlFiles()

        setattr(sql_alchemy_row, "content", data[3])
        setattr(sql_alchemy_row, "size", len(data))
        setattr(sql_alchemy_row, "name", data[0])
        setattr(sql_alchemy_row, "file_path", data[2])
        setattr(sql_alchemy_row, "download_flag", False)
        setattr(sql_alchemy_row, "upload_flag", False)
        setattr(sql_alchemy_row, "is_active", False)  
        setattr(sql_alchemy_row, "rule_content", data[4])
        setattr(sql_alchemy_row, "role_content", data[5])
        setattr(sql_alchemy_row, "local_storage", data[6])  
        session.add(sql_alchemy_row)
        try:
            session.commit()
            session.flush()
        except Exception as ex:
            session.rollback()
            message = f"File upload error {ex}"
            return jsonify(
                {
                    "code": 1,
                    "message": f"{message}",
                    "data": [],
                    "sqlTypes": None,
                }
            )

        return jsonify(
            {
                "code": 0,
                "message": "File uploaded successfully",
                "data": {},
            }
        )


    @app.route(
        "/ontimizeweb/services/rest/<path:path>",
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    )
    @cross_origin()
    @admin_required()
    def api_search(path):
        s = path.split("/")
        clz_name = s[0]
        clz_type = (
            None if len(s) == 1 else s[1]
        )  # [2] TODO customerType search advancedSearch defer(photo)customerTypeAggregate
        isSearch = s[len(s) - 1] == "search"
        method = request.method
        rows = []
        # CORS
        if method == "OPTIONS":
            return jsonify(success=True)

        if clz_name == "endsession":
            from flask import g

            sessionid = request.args.get("sessionid")
            if "access_token" in g and g.access_token == sessionid:
                g.pop("access_token")
            return jsonify({"code": 0, "data": {}, "message": None})

        if clz_name == "dynamicjasper":
            return _gen_report(request)

        if clz_name in ["listReports", "bundle", "reportstore"]:
            return jsonify({"code": 0, "data": {}, "message": None})

        if clz_name == "export":
            return gen_export(request)

        if request.path == "/ontimizeweb/services/rest/users/login":
            return login(request)

        # api_clz = api_map.get(clz_name)
        resource = find_model(clz_name)
        if resource == None:
            return jsonify(
                {"code": 1, "message": f"Resource {clz_name} not found", "data": None}
            )

        api_attributes = resource["attributes"]
        api_clz = resource["model"]

        payload = "{}" if request.data == b"" else json.loads(request.data)
        expressions, filter, columns, sqltypes, offset, pagesize, orderBy, data = (
            parsePayload(api_clz, payload)
        )
        result = {}
        if method == "GET":
            pagesize = 999  # if isSearch else pagesize
            return get_rows(
                request, api_clz, filter, orderBy, columns, pagesize, offset
            )

        if method in ["PUT", "PATCH"] and data:
            sql_alchemy_row = session.query(api_clz).filter(text(filter)).one()
            for key in DotDict(data):
                setattr(sql_alchemy_row, key, DotDict(data)[key])
            session.add(sql_alchemy_row)
            result = sql_alchemy_row
            # stmt = update(api_clz).where(text(filter)).values(data)

        if method == "DELETE":
            # stmt = delete(api_clz).where(text(filter))
            sql_alchemy_row = session.query(api_clz).filter(text(filter)).one()
            session.delete(sql_alchemy_row)
            result = sql_alchemy_row

        if method == "POST":
            if clz_name == "Entity" and clz_type == "reload":
                rebuild(request)
            if data != None:
                # this is an insert
                sql_alchemy_row = api_clz()
                row = DotDict(data)
                for attr in api_attributes:
                    name = attr["name"]
                    if getattr(row, name) != None:
                        setattr(sql_alchemy_row, name, row[name])
                session.add(sql_alchemy_row)
                result = sql_alchemy_row
                # stmt = insert(api_clz).values(data)

            else:
                if clz_name == "YamlFiles" and clz_type == "YamlFiles" \
                    and not request.path.endswith("advancedsearch") \
                    and not request.path.endswith("search"):
                    insertFile(request.json)
                elif clz_name == "YamlFiles" and clz_type in [
                    "importyaml",
                    "reloadyaml",
                    "downloadyaml",
                ]:
                    key = (
                        filter.split("=")[1]
                        if filter and "name" in filter
                        else "app_model.yaml"
                    )
                    active_files = (
                        session.query(models.YamlFiles).all()
                    )
                    for active in active_files:
                        state = active.name == str(key).strip().replace("'","",2)
                        setattr(active, "is_active", state)
                        session.add(active)
                        session.commit()
                        
                    key = key.replace("'", "", 2).strip()
                    key = key.replace('"', "", 2)
                    resp = (
                        session.query(models.YamlFiles)
                        .filter(models.YamlFiles.name == str(key))
                        .one()
                    )
                    if clz_type == "downloadyaml":
                        yaml_content, rule_content, security_content = (
                            export_yaml_to_file(_project_dir, resp)
                        )
                        try:
                            setattr(resp, "downloaded", yaml_content)
                            setattr(resp, "download_flag", True)
                            setattr(resp, "is_active", True)
                            session.add(resp)
                            session.commit()
                        except Exception as ex:
                            session.rollback()
                            return jsonify(
                                {
                                    "code": 1,
                                    "message": f"Yaml file {clz_type} error {ex}",
                                    "data": None,
                                }
                            )
                        try:
                            resp = (
                                session.query(models.YamlFiles)
                                .filter(models.YamlFiles.name == str(key))
                                .one()
                            )
                            setattr(resp, "rule_content", rule_content)
                            setattr(resp, "role_content", security_content)
                            session.add(resp)
                            session.commit()
                        except Exception as ex:
                            #session.rollback()
                            app_logger.debug(ex)
                            return jsonify(
                                {
                                    "code": 1,
                                    "message": f"Yaml file {clz_type} error {ex}",
                                    "data": None,
                                }
                            )
                    else:
                        yaml_content = (
                            resp.downloaded
                            if resp.downloaded != None and clz_type == "reloadyaml"
                            else resp.content
                        )
                        # yaml_content = request.data.decode("utf-8")
                        valuesYaml = yaml.safe_load(yaml_content)
                        process_yaml(
                            valuesYaml=valuesYaml, rule_content=resp.rule_content, role_content=resp.role_content, local_storage=resp.local_storage
                        )

                    data = {
                        "downloaded": yaml_content,
                        "rule_content": resp.rule_content,
                        "role_content": resp.role_content,
                        "local_storage": resp.local_storage,
                    }
                    return jsonify(
                        {
                            "code": 0,
                            "totalQueryRecordsNumber": 1,
                            "startRecordIndex": 1,
                            "message": f"Yaml file {clz_type}",
                            "data": data,
                        }
                    )
                # GET (sent as POST)
                # rows = get_rows_by_query(api_clz, filter, orderBy, columns, pagesize, offset)
                if "TypeAggregate" in clz_type:
                    return get_rows_agg(request, api_clz, clz_type, filter, columns)
                else:
                    pagesize = 999 if isSearch else pagesize
                    return get_rows(
                        request, api_clz, None, orderBy, columns, pagesize, offset
                    )
        try:
            session.commit()
            session.flush()
        except Exception as ex:
            session.rollback()
            return jsonify(
                {"code": 1, "message": f"{ex}", "data": [], "sqlTypes": None}
            )

        return jsonify(
            {"code": 0, "message": f"{method}:True", "data": result, "sqlTypes": None}
        )  # {f"{method}":True})

    def get_file_path(app_name: str) -> str:
        resp = (
            session.query(models.YamlFiles)
            .filter(models.YamlFiles.is_active == True)
            .one_or_none()
            )
        if resp:
            fp = getattr(resp,"file_path")
            return fp #TODO remove /ui
        return None
    def find_model(clz_name: str) -> any:
        clz_members = getMetaData()
        resources = clz_members.get("resources")
        for resource in resources:
            if resource == clz_name:
                return resources[resource]
        return None

    def login(request):
        url = f"{request.scheme}://{request.host}/api/auth/login"
        # no data is passed - uses basic auth in header
        # requests.post(url=url, headers=request.headers, json = {})
        username = ""
        password = ""
        auth = request.headers.get("Authorization", None)
        if auth and auth.startswith("Basic"):  # support basic auth
            import base64

            base64_message = auth[6:]
            print(f"auth found: {auth}")
            # base64_message = 'UHl0aG9uIGlzIGZ1bg=='
            base64_bytes = base64_message.encode("ascii")
            message_bytes = base64.b64decode(base64_bytes)
            message = message_bytes.decode("ascii")
            s = message.split(":")
            username = s[0]
            password = s[1]
        from security.authentication_provider.abstract_authentication_provider import (
            Abstract_Authentication_Provider,
        )
        from security.system.authentication import create_access_token

        authentication_provider: Abstract_Authentication_Provider = (
            Config.SECURITY_PROVIDER
        )
        if not authentication_provider:
            return (
                jsonify(
                    {"code": 1, "message": "No authentication provider configured"}
                ),
                401,
            )
        user = authentication_provider.get_user(username, password)
        if not user or not authentication_provider.check_password(
            user=user, password=password
        ):
            return jsonify({"code": 1, "message": "Wrong username or password"}), 401

        access_token = create_access_token(identity=user)  # serialize and encode
        from flask import g

        g.access_token = access_token
        # return jsonify(access_token=access_token)
        return jsonify(
            {
                "code": 0,
                "message": "Login Successful",
                "data": {"access_token": access_token},
            }
        )

    def get_rows_agg(request: any, api_clz, agg_type, filter, columns):
        key = api_clz.__name__
        resources = getMetaData(key)
        attributes = resources["resources"][key]["attributes"]
        list_of_columns = ""
        sep = ""
        attr_list = list(api_clz._s_columns)
        table_name = api_clz._s_type
        # api_clz.__mapper__.attrs #TODO map the columns to the attributes to build the select list
        for a in attributes:
            name = a["name"]
            t = a["type"]  # INTEGER or VARCHAR(N)
            # list_of_columns.append(api_clz._sa_class_manager.get(n))
            attr = a["attr"]
            # MAY need to do upper case compares
            if name in columns:
                list_of_columns = f"{list_of_columns}{sep}{name}"
                sep = ","
        sql = (
            f" count(*), {list_of_columns} from {table_name} group by {list_of_columns}"
        )
        print(sql)
        # TODO HARDCODED for now....
        data = {}
        if "customerTypeAggregate" == agg_type:
            data = {
                "data": [
                    {"AMOUNT": 24, "DESCRIPTION": "Normal"},
                    {"AMOUNT": 15, "DESCRIPTION": "VIP"},
                    {"AMOUNT": 36, "DESCRIPTION": "Other"},
                ]
            }
        elif "accountTypeAggregate" == agg_type:
            data = {
                "data": [
                    {"AMOUNT": 32, "ACCOUNTTYPENAME": "Savings", "ACCOUNTTYPEID": 1},
                    {"AMOUNT": 36, "ACCOUNTTYPENAME": "Checking", "ACCOUNTTYPEID": 0},
                    {"AMOUNT": 30, "ACCOUNTTYPENAME": "Payroll", "ACCOUNTTYPEID": 3},
                    {"AMOUNT": 23, "ACCOUNTTYPENAME": "Market", "ACCOUNTTYPEID": 2},
                ]
            }
        elif "employeeTypeAggregate" == agg_type:
            data = {
                "data": [
                    {"AMOUNT": 27, "EMPLOYEETYPENAME": "Manager"},
                    {"AMOUNT": 485, "EMPLOYEETYPENAME": "Employee"},
                ]
            }
        data["code"] = 0
        data["message"] = ""
        data["sqlType"] = {}
        # rows = session.query(text(sql)).all()
        # rows = session.query(models.Account.ACCOUNTTYPEID,func.count(models.Account.AccountID)).group_by(models.Account.ACCOUNTTYPEID).all()
        return data

    def get_rows(
        request: any,
        api_clz,
        filter: str,
        order_by: str,
        columns: list,
        pagesize: int,
        offset: int,
    ):
        # New Style
        key = api_clz.__name__.lower()
        resources = getMetaData(api_clz.__name__)
        attributes = resources["resources"][api_clz.__name__]["attributes"]
        list_of_columns = []
        for a in attributes:
            name = a["name"]
            col = a["attr"].columns[0]
            desc = col.description
            t = a["type"]  # INTEGER or VARCHAR(N)
            # MAY need to do upper case compares
            if desc in columns:
                list_of_columns.append((col, name))
            else:
                if name in columns:
                    list_of_columns.append(name)

        from api.system.custom_endpoint import CustomEndpoint

        request.method = "GET"
        r = CustomEndpoint(
            model_class=api_clz,
            fields=list_of_columns,
            filter_by=filter,
            pagesize=pagesize,
            offset=offset,
        )
        result = r.execute(request=request)
        service_type: str = Config.ONTIMIZE_SERVICE_TYPE
        return r.transform(
            service_type, key, result
        )  # JSONAPI or LAC or OntimizeEE ARGS.service_type

    def get_rows_by_query(api_clz, filter, orderBy, columns, pagesize, offset):
        # Old Style
        rows = []
        results = session.query(api_clz)  # or list of columns?

        if columns:
            # stmt = select(api_clz).options(load_only(Book.title, Book.summary))
            pass  # TODO

        if orderBy:
            results = results.order_by(text(parseOrderBy(orderBy)))

        if filter:
            results = results.filter(text(filter))

        results = results.limit(pagesize).offset(offset)

        for row in results.all():
            rows.append(row.to_dict())

        return rows

    def parseData(data: dict = None) -> str:
        # convert dict to str
        result = ""
        join = ""
        if data:
            for d in data:
                result += f'{join}{d}="{data[d]}"'
                join = ","
        return result

    def parseOrderBy(orderBy) -> str:
        # [{'columnName': 'SURNAME', 'ascendent': True}]
        result = ""
        if orderBy and len(orderBy) > 0:
            result = f"{orderBy[0]['columnName']}"  # TODO for desc
        return result

    def fix_payload(data, sqltypes):
        import datetime

        if sqltypes:
            for t in sqltypes:
                if sqltypes[t] == 91:  # Date
                    with contextlib.suppress(Exception):
                        my_date = float(data[t]) / 1000
                        data[t] = datetime.datetime.fromtimestamp(
                            my_date
                        )  # .strftime('%Y-%m-%d %H:%M:%S')
        """
        Converts SQLAlchemy result (mapped or raw) to dict array of un-nested rows

        Args:
            result (object): list of serializable objects (e.g., dict)

        Returns:
            list of rows as dicts
        """
        rows = []
        for each_row in result:
            row_as_dict = {}
            print(f"type(each_row): {type(each_row)}")
            if isinstance(
                each_row, sqlalchemy.engine.row.Row
            ):  # raw sql, eg, sample catsql
                key_to_index = each_row._key_to_index  # note: SQLAlchemy 2 specific
                for name, value in key_to_index.items():
                    row_as_dict[name] = each_row[value]
            else:
                row_as_dict = each_row.to_dict()  # safrs helper
            rows.append(row_as_dict)
        return rows

    @app.route("/exportyaml/<key>", methods=["GET"])
    def export_yaml(key: str = "app_model.yaml"):
        # Write the yaml to disk and update the database if name is found
        # GET curl "http://localhost:5656/exportyaml/{YamlFiles.name}"

        yaml_file, rule_content = export_yaml_to_file(_project_dir)
        try:
            sql_alchemy_row = (
                session.query(models.YamlFiles)
                .filter(models.YamlFiles.name == key)
                .one_or_none()
            )
            if sql_alchemy_row and sql_alchemy_row.downloaded is None:
                setattr(sql_alchemy_row, "downloaded", yaml_file)
                if rule_content:
                    setattr(sql_alchemy_row, "rule_content", rule_content)
                session.add(sql_alchemy_row)
                session.commit()
        except Exception as ex:
            print(ex)
            session.rollback()
            # return jsonify({"code": 1, "message": f"{ex}", "data": None})
        app_logger.debug(f"Yaml file written to ui/app_model_merge.yaml")
        app_logger.debug(f"Rule content written to ui/declare_logic_merge.py1")
        return {"downloaded": yaml_file, "rule_content": rule_content}

    @app.route("/importyaml/<key>", methods=["GET", "POST", "OPTIONS"])
    def load_yaml(key: str = "app_model.yaml"):
        """
        GET curl "http://localhost:5655/importyaml"
        POST  curl -X "POST" http://localhost:5655/importyaml -H "Content-Type: text/x-yaml" -d @app_model.yaml
        """
        if request.method == "GET" and int(key) == 0:
            with open(f"{_project_dir}/ui/app_model.yaml", "rt") as f:
                valuesYaml = yaml.safe_load(f.read())
                f.close()
        elif request.method == "GET" and int(key) > 0:
            from base64 import b64decode

            encoding = "utf-8"
            data = (
                session.query(models.YamlFiles)
                .filter(models.YamlFiles.name == str(key))
                .one()
            )
            yaml_content = data and data.content
            ##if not data.content.startswith('b')
            ##else str(b64decode(data.content), encoding=encoding)
            rule_content = data and data.rule_content
            
            if yaml_content:
                try:
                    valuesYaml = yaml.safe_load(yaml_content)
                    process_yaml(valuesYaml=valuesYaml)
                    return jsonify(
                        {"code": 0, "message": "Yaml file loaded", "data": None}
                    )
                except yaml.YAMLError as exc:
                    return jsonify({"code": 1, "message": f"Error loading yaml: {exc}"})
            if rule_content:
                merge_rules(rule_content)
            if local_storage:
                # TODO reorder the columns and visibility for each key
                pass
        elif request.method == "POST":
            data = (
                session.query(models.YamlFiles)
                .filter(models.YamlFiles.name == str(key))
                .one()
            )
            yaml_content = data and data.content
            rule_content = data and data.rule_content
            app_content = data and data.app_content
            rbac_content = data and data.rbac_content
            local_storage = data and data.local_storage
            # yaml_content = request.data.decode("utf-8")
            valuesYaml = yaml.safe_load(yaml_content)
            process_yaml(
                valuesYaml=valuesYaml,
                rule_content=rule_content,
                rbac_content=rbac_content,
                local_storage=local_storage,
            )
            return jsonify({"code": 0, "message": "Yaml file loaded", "data": None})

    def _gen_report(request) -> any:
        payload = json.loads(request.data)

        print(payload)
        if len(payload) == 3:
            return jsonify({})

        entity = payload["entity"]
        resource = find_model(entity)
        api_clz = resource["model"]
        resources = getMetaData(api_clz.__name__)
        attributes = resources["resources"][api_clz.__name__]["attributes"]

        return gen_report(api_clz, request, _project_dir, payload, attributes)

    def clonerow(request) -> any:
        payload = json.loads(request.data)
        print("clonerow", payload["filter"])  # TODO
        return jsonify({"code": 0, "message": "clonerow", "data": {}})

    # http://localhost:5656/ontimizeweb/services/qsallcomponents-jee/services/rest/customers/customerType/search
    # https://try.imatia.com/ontimizeweb/services/qsallcomponents-jee/services/rest/customers/customerType/search

    def api_search_orig(path):
        s = path.split("/")
        clz_name = s[0]
        clz_type = (
            None if len(s) == 1 else s[1]
        )  # [2] TODO customerType search advancedSearch defer(photo)customerTypeAggregate

        method = request.method
        rows = []
        # CORS
        if method == "OPTIONS":
            return jsonify(success=True)

        if clz_name == "Entity" and clz_type == "clonerow":
            return clonerow(request)

        if clz_name == "dynamicjasper":
            return _gen_report(request)

        if clz_name in ["listReports", "bundle", "reportstore"]:
            return jsonify({"code": 0, "data": {}, "message": None})

        if clz_name == "export":
            return gen_export(request)

        if clz_type == "importyaml":
            return load_yaml()

        # if clz_type == "exportyaml":
        #    return dump_yaml()

        if clz_type == "upload":
            # TODO get full path and filename from request or store locally and read file
            file_name = f"{_project_dir}/ui/app_model.yaml"
            return _process_yaml(filename=file_name)

        # api_clz = api_map.get(clz_name)
        resource = find_model(clz_name)
        api_attributes = resource["attributes"]
        api_clz = resource["model"]

        payload = json.loads(request.data)
        filter, columns, sqltypes, offset, pagesize, orderBy, data = parsePayload(
            payload
        )
        result = {}
        if method in ["PUT", "PATCH"]:
            sql_alchemy_row = session.query(api_clz).filter(text(filter)).one()
            for key in DotDict(data):
                setattr(sql_alchemy_row, key, DotDict(data)[key])
            session.add(sql_alchemy_row)
            result = sql_alchemy_row
            # stmt = update(api_clz).where(text(filter)).values(data)

        if method == "DELETE":
            # stmt = delete(api_clz).where(text(filter))
            sql_alchemy_row = session.query(api_clz).filter(text(filter)).one()
            session.delete(sql_alchemy_row)
            result = sql_alchemy_row

        if method == "POST":
            if data != None:
                # this is an insert
                sql_alchemy_row = api_clz()
                row = DotDict(data)
                for attr in api_attributes:
                    name = attr["name"]
                    if getattr(row, name) != None:
                        setattr(sql_alchemy_row, name, row[name])
                session.add(sql_alchemy_row)
                result = sql_alchemy_row
                # stmt = insert(api_clz).values(data)

            else:
                # GET (sent as POST)
                # rows = get_rows_by_query(api_clz, filter, orderBy, columns, pagesize, offset)
                if "TypeAggregate" in clz_type:
                    return get_rows_agg(request, api_clz, clz_type, filter, columns)
                else:
                    return get_rows(
                        request, api_clz, None, orderBy, columns, pagesize, offset
                    )
                    # return _get_rows(request, api_clz, filter, orderBy, columns, pagesize, offset)

        try:
            session.commit()
            session.flush()
        except Exception as ex:
            session.rollback()
            msg = f"{ex.message if hasattr(ex, 'message') else ex}"
            return jsonify(
                {"code": 1, "message": f"{msg}", "data": [], "sqlTypes": None}
            )

        return jsonify(
            {"code": 0, "message": f"{method}:True", "data": result, "sqlTypes": None}
        )  # {f"{method}":True})

    def find_model(clz_name: str) -> any:
        clz_members = getMetaData()
        resources = clz_members.get("resources")
        for resource in resources:
            if resource == clz_name:
                return resources[resource]
        return None

    def get_rows_agg(request: any, api_clz, agg_type, filter, columns):
        key = api_clz.__name__
        resources = getMetaData(key)
        attributes = resources["resources"][key]["attributes"]
        list_of_columns = ""
        sep = ""
        attr_list = list(api_clz._s_columns)
        table_name = api_clz._s_type
        # api_clz.__mapper__.attrs #TODO map the columns to the attributes to build the select list
        for a in attributes:
            name = a["name"]
            t = a["type"]  # INTEGER or VARCHAR(N)
            # list_of_columns.append(api_clz._sa_class_manager.get(n))
            attr = a["attr"]
            # MAY need to do upper case compares
            if name in columns:
                list_of_columns = f"{list_of_columns}{sep}{name}"
                sep = ","
        sql = (
            f" count(*), {list_of_columns} from {table_name} group by {list_of_columns}"
        )
        print(sql)
        # TODO HARDCODED for now....
        data = {}
        if "customerTypeAggregate" == agg_type:
            data = {
                "data": [
                    {"AMOUNT": 24, "DESCRIPTION": "Normal"},
                    {"AMOUNT": 15, "DESCRIPTION": "VIP"},
                    {"AMOUNT": 36, "DESCRIPTION": "Other"},
                ]
            }
        elif "accountTypeAggregate" == agg_type:
            data = {
                "data": [
                    {"AMOUNT": 32, "ACCOUNTTYPENAME": "Savings", "ACCOUNTTYPEID": 1},
                    {"AMOUNT": 36, "ACCOUNTTYPENAME": "Checking", "ACCOUNTTYPEID": 0},
                    {"AMOUNT": 30, "ACCOUNTTYPENAME": "Payroll", "ACCOUNTTYPEID": 3},
                    {"AMOUNT": 23, "ACCOUNTTYPENAME": "Market", "ACCOUNTTYPEID": 2},
                ]
            }
        elif "employeeTypeAggregate" == agg_type:
            data = {
                "data": [
                    {"AMOUNT": 27, "EMPLOYEETYPENAME": "Manager"},
                    {"AMOUNT": 485, "EMPLOYEETYPENAME": "Employee"},
                ]
            }
        data["code"] = 0
        data["message"] = ""
        data["sqlType"] = {}
        # rows = session.query(text(sql)).all()
        # rows = session.query(models.Account.ACCOUNTTYPEID,func.count(models.Account.AccountID)).group_by(models.Account.ACCOUNTTYPEID).all()
        return data

    def get_rows_by_query(api_clz, filter, orderBy, columns, pagesize, offset):
        # Old Style
        rows = []
        results = session.query(api_clz)  # or list of columns?

        if columns:
            # stmt = select(api_clz).options(load_only(Book.title, Book.summary))
            pass  # TODO

        if orderBy:
            results = results.order_by(text(parseOrderBy(orderBy)))

        if filter:
            results = results.filter(text(filter))

        results = results.limit(pagesize).offset(offset)

        for row in results.all():
            rows.append(row.to_dict())

        return rows

    def parseData(data: dict = None) -> str:
        # convert dict to str
        result = ""
        join = ""
        if data:
            for d in data:
                result += f'{join}{d}="{data[d]}"'
                join = ","
        return result

    def parseOrderBy(orderBy) -> str:
        # [{'columnName': 'SURNAME', 'ascendent': True}]
        result = ""
        if orderBy and len(orderBy) > 0:
            result = f"{orderBy[0]['columnName']}"  # TODO for desc
        return result

    def fix_payload(data, sqltypes):
        import datetime

        if sqltypes:
            for t in sqltypes:
                if sqltypes[t] == 91:  # Date
                    with contextlib.suppress(Exception):
                        my_date = float(data[t]) / 1000
                        data[t] = datetime.datetime.fromtimestamp(
                            my_date
                        )  # .strftime('%Y-%m-%d %H:%M:%S')

    # Process the yaml file (load SQLite)
    def process_yaml(
        valuesYaml: str, rule_content: str = None, role_content: str = None, local_storage: any = None
    ):
        # Clean the database out - this is destructive

        delete_sql(models.TabGroup)
        delete_sql(models.GlobalSetting)
        delete_sql(models.RuleDerivation)
        delete_sql(models.EntityAttr)
        delete_sql(models.RuleConstraint)
        delete_sql(models.RuleEvent)
        delete_sql(models.Template)
        delete_sql(models.Root)
        delete_sql(models.GrantRole)
        delete_sql(models.RbacRole)
        delete_sql(models.Page)
        delete_sql(models.MenuGroup)
        delete_sql(models.MenuItem)
        delete_sql(models.Application)
        delete_sql(models.Entity)

        rules = []
        roles = []
        grants = []
        try:
            if rule_content:
                from api.api_discovery.rule_parser import get_rules_from_content
                rules = get_rules_from_content(rule_content)
        except Exception as ex:
            print(f"<<<<Rules {ex} >>>>>")
        try:
            if role_content:
                from api.api_discovery.security_parser import get_security
                roles = get_security(role_content)  
                from api.api_discovery.security_parser import get_grants
                grants = get_grants(role_content)
        except Exception as ex:
            print(f"<<<< Security {ex} >>>>>")
            
        insert_template()
        insert_styles(valuesYaml)
        insert_entities(valuesYaml, rules, local_storage)
        insert_root(valuesYaml)
        
        if rule_content:
            insert_rules(rules)
        else:
            insert_rules_from_yaml(valuesYaml)
            
        if role_content:
            insert_roles(roles)
            insert_grants(grants)
        else:
            insert_roles_from_yaml(valuesYaml)
            insert_grants_from_yaml(valuesYaml)
        
        insert_application(valuesYaml)
        
        return jsonify(valuesYaml)

    def delete_sql(clz):
        try:
            num_rows_deleted = db.session.query(clz).delete()
            print(clz, num_rows_deleted)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            raise ex

    def insert_entities(valuesYaml, rules, local_storage: any = None):
        entities = valuesYaml["entities"]
        for entity in entities:
            m_entity = models.Entity()
            each_entity = valuesYaml["entities"][entity]
            print(entity, each_entity)
            m_entity.name = each_entity["type"]
            m_entity.title = get_value(each_entity, "title", entity)
            m_entity.favorite = get_value(each_entity, "favorite")
            m_entity.pkey = str(get_value(each_entity, "primary_key"))
            m_entity.info_list = get_value(each_entity, "info_list")
            m_entity.info_show = get_value(each_entity, "info_show")
            m_entity.exclude = get_boolean(each_entity, "exclude", False)
            m_entity.new_template = get_value(
                each_entity, "new_template", "new_template.html"
            )
            m_entity.home_template = get_value(
                each_entity, "home_template", "home_template.html"
            )
            m_entity.detail_template = get_value(
                each_entity, "detail_template", "detail_template.html"
            )
            m_entity.mode = get_value(each_entity, "mode", "tab")
            m_entity.menu_group = get_value(each_entity, "group", "data")

            try:
                session.add(m_entity)
                session.commit()
            except Exception as ex:
                session.rollback()
                raise ex

        # Attributes
        for entity in entities:
            each_entity_yaml = valuesYaml["entities"][entity]
            entity_type = entities[entity]["type"]
            insert_entity_attrs(entity, entity_type, each_entity_yaml, rules, local_storage)

        # Tab Groups
        for entity in entities:
            each_entity_yaml = valuesYaml["entities"][entity]
            entity_type = entities[entity]["type"]
            insert_tab_groups(entity, entity_type, each_entity_yaml)

    def insert_root(valuesYaml):
        about = valuesYaml["about"]
        api_root = valuesYaml["api_root"]
        authentication = valuesYaml["authentication"]
        root = models.Root()  # session.query(models.Root).one_or_none()
        root.id = 1
        root.about_date = about["date"]
        root.about_changes = about["recent_changes"]
        root.api_root = api_root
        root.api_auth_type = "endpoint"
        root.api_auth = (
            authentication["endpoint"]
            if "endpoint" in authentication
            else authentication
        )
        try:
            session.add(root)
            session.commit()
        except Exception as ex:
            print(ex)
            # session.rollback()

    def insert_template():
        #TODO - use the html name (fix) and load from file and allow edits/writes
        '''
        This is only for input templates on Attributes
        '''
        templates = [
            ("checkbox", "o_checkbox.html"),
            {"check_circle", "check_circle.html"},
            ("combo", "o_combo_input.html"),
            ("currency", "currency_template.html"),
            ("date", "date_template.html"),
            ("email", "email_template.html"),
            ("file", "file_template.html"),
            ("html", "html_template.html"),
            ("integer", "integer_template.html"),
            ("list", "list-picker.html"),
            ("nif", "o_nif_input.html"),
            ("password", "password_template.html"),
            ("percent", "percent_template.html"),
            ("phone", "phone_template.html"),
            ("real", "real_template.html"),
            ("text", "text_template.html"),
            ("textarea", "textarea_template.html"),
            ("time", "time_template.html"),
            ("timestamp", "timestamp_template.html"),
            ("toggle", "o_slide_toggle.html"),
        ]
        for name, value in templates:
            m_template = models.Template()
            m_template.name = name
            m_template.file_name = value
            m_template.description = get_template(name, value)
            try:
                session.add(m_template)
                session.commit()
            except Exception as ex:
                print(ex)
    def get_template(name, value):
        with open(f"{_project_dir}/ui/yaml/templates/{value}", "r") as f:
            return f.read()
    def insert_roles(roles: list):
        for role in roles:
            m_role = models.RbacRole()
            setattr(m_role,"name" , role["to_role"])
            setattr(m_role,"can_read" , role["can_read"]== True)
            setattr(m_role,"can_insert" , role["can_insert"]== True)
            setattr(m_role,"can_update" , role["can_update"]== True)
            setattr(m_role,"can_delete" , role["can_delete"]== True)
            try:
                session.add(m_role)
                session.commit()
            except Exception as ex:
                print(ex)
    def insert_grants(grants: list):
        for role in grants:
            m_role = models.GrantRole()
            setattr(m_role,"entity_name" , role["on_entity"])
            setattr(m_role,"role_name" , role["to_role"])
            setattr(m_role,"can_read" , role["can_read"]== True)
            setattr(m_role,"can_insert" , role["can_insert"]== True)
            setattr(m_role,"can_update" , role["can_update"]== True)
            setattr(m_role,"can_delete" , role["can_delete"]== True)
            if role["filter"] != "":
                setattr(m_role,"filter" , role["filter"])
            if role["filter_debug"] != "":
                setattr(m_role,"filter_debug" , role["filter_debug"])
            try:
                session.add(m_role)
                session.commit()
            except Exception as ex:
                print(ex)
    def insert_rules(rules: list):
        for rule in rules:
            print(rule)
            if rule["entity"] == "all":
                continue
            if rule["type"] == "constraint":
                sql_alchemy_row = models.RuleConstraint()
                setattr(sql_alchemy_row, "rule", rule["rule"])
                setattr(sql_alchemy_row, "entity_name", rule["entity"])
                try:
                    session.add(sql_alchemy_row)
                    session.commit()
                except Exception as ex:
                    print(f"Error adding constraint rule {rule} {ex}")
                    continue
            elif rule["type"].endswith("_event"):
                sql_alchemy_row = models.RuleEvent()
                setattr(sql_alchemy_row, "rule", rule["rule"])
                setattr(sql_alchemy_row, "entity_name", rule["entity"])
                setattr(sql_alchemy_row, "event_type", rule["type"])
                try:
                    session.add(sql_alchemy_row)
                    session.commit()
                except Exception as ex:
                    print(f"Error adding event rule {rule} {ex}")
                    continue
            else:
                sql_alchemy_row = models.RuleDerivation()

                setattr(sql_alchemy_row, "rule", rule["rule"])
                setattr(sql_alchemy_row, "entity_name", rule["entity"])
                setattr(sql_alchemy_row, "derivation_type", rule["type"])
                setattr(sql_alchemy_row, "derive_column", rule["attr"])
                try:
                    session.add(sql_alchemy_row)
                    session.commit()
                    # if rule['attr']:
                    # update_entity_attr(rule["entity"], rule["rule"], rule['attr'])
                except Exception as ex:
                    print(f"Error adding derivations rule {rule} {ex}")
                    continue

    def parse_derivation_rule(rule: dict) -> str:
        derive_column, expression = None
        if not rule:
            return derive_column, expression
        if rule.index("derive=") > 0:
            derive_column = rule.split("=")[1].split(",")[0]
        elif rule.index("models.") > 0:
            derive_column = rule.split("models.")[1].split(".")[1].split(",")[0]
        try:
            if rule["type"] == "sum":
                expression = (
                    rule.split("as_sum_of")[1].replace("=models.", "").replace(")", "")
                )
            elif rule["type"] == "count":
                expression = (
                    rule.split("where")[0].replace("=models.", "").replace(")", "")
                )
            elif rule["type"] == "formula":
                expression = (
                    rule.split("as_expression")[1]
                    .replace("=models.", "")
                    .replace(")", "")
                )
            elif rule["type"] == "copy":  # from_parent
                expression = rule.split("from_parent=")[1].replace(")", "")
        except Exception as e:
            print(e)
        return derive_column, expression

    def update_entity_attr(entity: str, derivation: str, rule_attr: str):
        entity_attr = (
            session.query(models.EntityAttr)
            .filter(models.EntityAttr.entity_name == entity)
            .order_by(models.EntityAttr.create_date.desc())
            .all()
        )
        for attr in entity_attr:
            if attr.label == rule_attr:
                attr.derivation = derivation
                try:
                    session.add(attr)
                    session.commit()
                    return
                except Exception as ex:
                    print(f"Error adding derivations rule {attr} {ex}")

    def insert_roles_from_yaml(valuesYaml: dict):
        for role in valuesYaml["roles"]:
            m_role = models.RbacRole()
            setattr(m_role,"name" , role["to_role"])
            setattr(m_role,"can_read" , role["can_read"])
            setattr(m_role,"can_insert" , role["can_insert"])
            setattr(m_role,"can_update" , role["can_update"])
            setattr(m_role,"can_delete" , role["can_delete"])
            try:
                session.add(m_role)
                session.commit()
            except Exception as ex:
                print(ex)
    def insert_grants_from_yaml(valuesYaml: dict):
        for role in valuesYaml["grants"]:
            m_role = models.GrantRole()
            setattr(m_role,"entity_name" , role["on_entity"])
            setattr(m_role,"role_name" , role["to_role"])
            setattr(m_role,"can_read" , role["can_read"])
            setattr(m_role,"can_insert" , role["can_insert"])
            setattr(m_role,"can_update" , role["can_update"])
            setattr(m_role,"can_delete" , role["can_delete"])
            setattr(m_role,"filter" , role["filter"])
            setattr(m_role,"filter_debug" , role["filter_debug"])
            try:
                session.add(m_role)
                session.commit()
            except Exception as ex:
                print(ex)
    def insert_rules_from_yaml(valuesYaml: dict):
        for entity in valuesYaml["entities"]:
            rules = (
                valuesYaml["entities"][entity]["rules"]
                if "rules" in valuesYaml["entities"][entity]
                else None
            )
            if rules:
                for constraint in rules["contraints"]:
                    m_rule = models.RuleConstraint()
                    m_rule.entity_name = entity
                    m_rule.rule = constraint

                try:
                    session.add(m_rule)
                    session.commit()
                except Exception as ex:
                    # session.rollback()
                    print(ex)

                for event in rules["events"]:
                    m_rule = models.RuleEvent()
                    m_rule.entity_name = entity
                    m_rule.rule = event
                    type = event.split("Rule.")[1].split("(")[0]
                    m_rule.event_type = type

                try:
                    session.add(m_rule)
                    session.commit()
                except Exception as ex:
                    # session.rollback()
                    print(ex)

            for column in valuesYaml["entities"][entity]["columns"]:
                rule = column["derivation"] if "derivation" in column else None
                if rule:
                    m_rule = models.RuleDerivation()
                    m_rule.entity_name = entity
                    m_rule.rule = rule
                    type = rule.split("Rule.")[1].split("(")[0]
                    m_rule.derivation_type = type
                    # derviation, expression = parse_derivation_rule(rule)

                    try:
                        session.add(m_rule)
                        session.commit()
                    except Exception as ex:
                        # session.rollback()
                        print(ex)

    def insert_application(valuesYaml: any):
        try:
    
            name = "New Application"
            file_path = "/foo"
            app_name = "app"
            application = models.Application()
            setattr(application,"name",name)
            setattr(application,"app_short_name",app_name)
            #setattr(application,"description",file_path)
            session.add(application)
            session.commit()
        except Exception as ex:
            print(f"application error {ex}")
        #insert_menu_group(application, valuesYaml)
        menu_group = models.MenuGroup()
        menu_group.application_id = application.id
        menu_group.icon = "edit_square"
        menu_group.menu_name = "data"
        menu_group.menu_id = "data"
        menu_group.opened = True
        #menu_group.menu_title = ""
        try:
            session.add(menu_group)
            session.commit()
        except Exception as ex:
            print(f"menu_group error {ex}")
            
        #insert_menu_item(app, valuesYaml)
        entities = valuesYaml["entities"]
        for entity in entities:
            menu_item = models.MenuItem()
            menu_item.menu_group_id = menu_group.id
            menu_item.entity_name = entity
            menu_item.menu_name = entity 
            menu_item.template_name = "module.jinja"
            menu_item.icon ="edit_square"
            try:
                session.add(menu_item)
                session.commit()
                col_list = []
                for col in valuesYaml["entities"][entity]["columns"]:
                    col_list.append(col["name"])
                for page_name in ['new', 'home', 'detail']: 
                    page = models.Page()
                    page.menu_item_id = menu_item.id
                    page.title = entity
                    page.page_name = page_name
                    page.template_name = f"{page_name}_template.html"
                    page.columns = ",".join(col_list)   
                    page.visible_columns = ",".join(col_list)  
                    page.include_children = True
                    session.add(page)
                    session.commit()
            except Exception as ex:
                print(f"menu_item error {ex}")
        
    def get_value(obj: any, name: str, default: any = None):
        try:
            return obj[name]
        except Exception as ex:
            return default

    def get_boolean(obj: any, name: str, default: bool = True):
        try:
            if isinstance(obj[name], bool):
                return obj[name]
            else:
                return obj[name] in ["true", "True", "1"]
        except Exception as ex:
            return default

    def insert_tab_groups(entity, entity_type, each_entity_yaml):
        tab_groups = (
            each_entity_yaml["tab_groups"] if "tab_groups" in each_entity_yaml else []
        )
        for tab_group in tab_groups:
            m_tab_group = models.TabGroup()
            print(entity, f" tab_group: {tab_group}")
            m_tab_group.entity_name = entity
            m_tab_group.direction = tab_group["direction"]
            m_tab_group.tab_entity = tab_group["resource"]
            m_tab_group.fkeys = str(tab_group["fks"])
            m_tab_group.name = tab_group.get("name")
            m_tab_group.label = tab_group.get("label") or tab_group.get("name")
            m_tab_group.exclude = get_boolean(tab_group, "exclude", False)

            try:
                session.add(m_tab_group)
                session.commit()
            except Exception as ex:
                session.rollback()
                print(ex)

    def insert_entity_attrs(entity, entity_type, each_entity_yaml, rules, local_storage: any = None):
        columns = []
        yaml_columns = sort_yaml_columns(entity, entity_type, each_entity_yaml["columns"], local_storage)
        for attr in yaml_columns:
            if attr not in columns:
                columns.append(attr)
                m_entity_attr = models.EntityAttr()
                print(entity, f": {attr}")  # merge metadata into attr
                m_entity_attr.entity_name = entity_type
                m_entity_attr.attr = get_value(attr, "name")
                m_entity_attr.label = get_value(attr, "label", attr["name"])
                m_entity_attr.template_name = get_value(attr, "template", "text")
                m_entity_attr.thistype = get_value(attr, "type", "VARCHAR")
                m_entity_attr.isrequired = get_boolean(attr, "required", False)
                m_entity_attr.issearch = get_boolean(attr, "search", False)
                m_entity_attr.isort = get_boolean(attr, "sort", False)
                m_entity_attr.isenabled = get_boolean(attr, "enabled", True)
                m_entity_attr.exclude = get_boolean(attr, "exclude", False)
                m_entity_attr.tooltip = get_value(
                    attr, "tooltip", f'Insert {attr["name"]}'
                )
                m_entity_attr.visible = get_boolean(attr, "visible", True)
                if get_value(attr, "default_value"):
                    m_entity_attr.default_value = get_value(attr, "default_value", "")
                if get_value(attr, "derivation"):
                    derivation = get_value(attr, "derivation", "")
                else:
                    derivation = None
                    for rule in rules:
                        if rule["entity"] == entity and rule["attr"] == attr["name"]:
                            derivation = rule["rule"]
                            derivation = derivation if derivation is not None else ""
                            break
                m_entity_attr.derivation = get_value(attr, "derivation", derivation)
            try:
                session.add(m_entity_attr)
                session.commit()
            except Exception as ex:
                session.rollback()
                # raise ex
                print(ex)

                # parse_derivation_rule(sql_alchemy_row)
                # if rule['attr']:
                #        update_entity_attr(rule["entity"], rule["rule"], rule['attr'])
    def sort_yaml_columns(entity, entity_type, columns, local_storage):
        #reorder the columns and visibility for each key in local_storage imported from settings
        if local_storage:
            ls = json.loads(local_storage)
            for items in ls:
                if items["key"] == f"{entity}Table_/main/{entity}":
                    display_cols = items["oColumns-display"]
                    sorted_cols = []
                    for col in display_cols:
                        #print(col["attr"], col["visible"])
                        for c in columns:
                            if c["name"] == col["attr"]:
                                c["visible"] = col["visible"]
                                sorted_cols.append(c)
                    return sorted_cols
            
        return columns
    def insert_styles(valuesYaml):
        style_guide = valuesYaml["settings"]["style_guide"]
        print(f"style_guide: {style_guide}")
        for style in style_guide:
            global_setting = models.GlobalSetting()
            print(f"{style}:{style_guide[style]}")
            global_setting.name = style
            global_setting.value = str(style_guide[style])
            session.add(global_setting)
        try:
            session.commit()
        except Exception as ex:
            raise ex


def write_file(source: list, file_name: str) -> any:
    with open(file_name, "w") as file:
        for l in source:
            file.writelines(f"{l}\n")
    with open(file_name, "r") as file:
        return file.read()
    return None


def write_yaml_file(source: str, file_name: str) -> any:
    try:
        with open(file_name, "w") as file:
            yaml.safe_dump(source, file, default_flow_style=False)
            # file.write(source)
        with open(file_name, "r") as file:
            return file.read()
    except Exception as ex:
        print(f"Error writing yaml file {file_name} with exception: {ex}")
    return source


def export_yaml_to_file(project_dir: str, yaml_file_row: dict = None):
    entities = read(models.Entity)
    attrs = read(models.EntityAttr)
    tabs = read(models.TabGroup)
    settings = read(models.GlobalSetting)
    root = read(models.Root)
    rule_events = read(models.RuleEvent)
    rule_constraints = read(models.RuleConstraint)
    rule_derivations = read(models.RuleDerivation)
    rbac_content = read(models.RbacRole)
    grant_content = read(models.GrantRole)
    security_output = build_security_json(rbac_content, grant_content)

    output = build_json(
        entities, attrs, tabs, settings, root, rule_events, rule_constraints, security_output
    )
    yaml_fn = f"{project_dir}/ui/app_model_merge.yaml"
    logic_fn = f"{project_dir}/ui/declare_logic_merge.py1"
    security_fn = f"{project_dir}/ui/declare_security.py1"
    logic_output = build_logic(attrs, rule_constraints, rule_events, rule_derivations)
    security_output = build_security(output["user_roles"], output["grants"])
    lo = write_file(logic_output, file_name=logic_fn)
    yo = write_yaml_file(output, file_name=yaml_fn)
    so = write_file(security_output, file_name=security_fn)
    if yaml_file_row and getattr(yaml_file_row,"file_path"):
        yaml_fn = f"{getattr(yaml_file_row,"file_path")}/app_model.yaml"
        write_yaml_file(output, file_name=yaml_fn)
    return yo, lo, so


def rows_to_dict(result: any) -> list:
    """
    Converts SQLAlchemy result (mapped or raw) to dict array of un-nested rows

    Args:
        result (object): list of serializable objects (e.g., dict)

    Returns:
        list of rows as dicts
    """
    rows = []
    for each_row in result:
        row_as_dict = {}
        print(f"type(each_row): {type(each_row)}")
        if isinstance(
            each_row, sqlalchemy.engine.row.Row
        ):  # raw sql, eg, sample catsql
            key_to_index = each_row._key_to_index  # note: SQLAlchemy 2 specific
            for name, value in key_to_index.items():
                row_as_dict[name] = each_row[value]
        else:
            row_as_dict = each_row.to_dict()  # safrs helper
        rows.append(row_as_dict)
    return rows


def read(clz) -> list:
    return rows_to_dict(session.query(clz).all())


def clean(rule: str) -> str:
    rule = rule.replace('"', "'", 10)
    rule = rule.replace("\n", "", 10)
    return f"    {rule}"


def append_calling_logic(rule_constraints, rule_events, rule_derivations) -> list:
    # Placeholder function to append calling logic
    # You can implement the actual logic here

    logic = []
    logic.extend(find_fn(rule["rule"]) for rule in rule_constraints)
    logic.extend(find_fn(rule["rule"]) for rule in rule_events)
    logic.extend(find_fn(rule["rule"]) for rule in rule_derivations)
    result = ["# Rule Function Calling"]
    for l in logic:
        if len(l) > 0:
            result.extend((l, "           pass"))
    return result


def find_fn(rule: str) -> str:
    event = []
    # ['#def calling_fn(row: model.EntityName, old_row: model.EntityName, logic_row:LogicRow):','#   pass']
    entity_name = ""
    for part in rule.split("="):
        if part.split(",")[0].startswith("models."):
            entity_name = part.split(",")[0].split(".")[1].strip()
            break
    for part in rule.split(","):
        if "calling" in part:
            fn_name = part.split("=")[1].strip()
            event = f"    def {fn_name[:-1]}(row: model.{entity_name}, old_row: model.{entity_name}, logic_row:LogicRow):"
    return event

def build_security(rbac_content: list, grant_content: list) -> str:
    security = ["from security.system.authorization import Grant, Security, Security, DefaultRolePermission, GlobalFilter"]
    security.append("class Roles():")
    for role in rbac_content:
        security.append(f'    {role} = "{role}"')
    security.append("# Roles")
    for r in rbac_content:
        role = rbac_content[r]
        security.append(f"DefaultRolePermission(to_role=Roles.{r}, can_read={role['can_read']}, can_insert={role['can_insert']}, can_update={role['can_update']}, can_delete={role['can_delete']})")
    security.append("# Grants")
    for g in grant_content:
        grant = grant_content[g]
        s = g.split("_")
        entity_name = s[0]
        role_name = s[1]
        security.append(f"Grant(models.{entity_name}, to_role=Roles.{role_name}, can_read={grant['can_read']}, can_insert={grant['can_insert']}, can_update={grant['can_update']}, can_delete={grant['can_delete']}, filter={grant['filter']}, filter_debug={grant['filter_debug']})")   
        
    return security
    
def build_logic(attrs, rule_constraints, rule_events, rule_derivations) -> str:
    logic = ["from logic_bank.logic_bank import Rule"]
    logic.extend(append_calling_logic(rule_constraints, rule_events, rule_derivations))
    logic.append("# Constraints")
    logic.extend(clean(rule["rule"]) for rule in rule_constraints)
    logic.append("# Events")
    logic.extend(clean(rule["rule"]) for rule in rule_events)
    logic.append("# Derivations")
    logic.extend(clean(rule["rule"]) for rule in rule_derivations)
    logic.extend(clean(attr["derivation"]) for attr in attrs if attr["derivation"])

    return logic


def build_security_json(rbac_content: list, grant_content: list) -> dict:
    """
    Builds a security JSON structure from role-based access control (RBAC) and grant content.

    This function takes two lists: one containing role definitions and another containing grant definitions. It constructs a JSON object that organizes roles and grants, detailing their permissions and attributes.

    Args:
        rbac_content (list): A list of dictionaries representing roles, each containing keys such as 'name', 'description', 'can_read', 'can_insert', 'can_update', and 'can_delete'.
        grant_content (list): A list of dictionaries representing grants, each containing keys such as 'entity_name', 'role_name', 'description', 'can_read', 'can_insert', 'can_update', 'can_delete', 'filter', and 'filter_debug'.

    Returns:
        dict: A dictionary containing two keys: 'roles' and 'grants', each mapping to their respective structured data.
    """

    output = {}
    output["roles"] = {
        r["name"]: {
            "can_read": r["can_read"] == True,
            "can_insert": r["can_insert"] == True,
            "can_update": r["can_update"] == True,
            "can_delete": r["can_delete"] == True,
        }
        for r in rbac_content
    }
    output["grants"] = {
        f'{r["entity_name"]}_{r["role_name"]}': {
            "can_read": r["can_read"] == True,
            "can_insert": r["can_insert"] == True,
            "can_update": r["can_update"] == True,
            "can_delete": r["can_delete"] == True,
            "filter": r["filter"],
            "filter_debug": r["filter_debug"],
        }
        for r in grant_content
    }
    return output

def build_json(
    entities: list,
    attrs: list,
    tabs: list,
    settings: list,
    root: list,
    rule_events: list,
    rule_constraints: list,
    security_output: dict,
) -> any:
    """
    Constructs a structured JSON representation of various application entities and their attributes.

    This function aggregates information from multiple sources, including entities, attributes, tabs, settings, and rules, to create a comprehensive JSON output. The resulting structure is intended for use in API responses, providing detailed metadata about the application's configuration and capabilities.

    Args:
        entities (list): A list of dictionaries representing entities, each containing keys such as 'name', 'title', 'pkey', and optional template and configuration fields.
        attrs (list): A list of dictionaries representing attributes associated with entities, including keys like 'entity_name', 'attr', 'label', 'template_name', and various flags.
        tabs (list): A list of dictionaries representing tab groups for entities, including keys such as 'entity_name', 'direction', 'tab_entity', and foreign keys.
        settings (list): A list of dictionaries representing application settings, each containing keys like 'name' and 'value'.
        root (list): A list of dictionaries containing root-level metadata, including keys such as 'about_date', 'about_changes', 'api_root', 'api_auth_type', and 'api_auth'.
        rule_events (list): A list of dictionaries representing event rules associated with entities.
        rule_constraints (list): A list of dictionaries representing constraint rules associated with entities.
        security_output (dict): A dictionary containing structured information about roles and grants, organized for API consumption.
            roles (list): A list of dictionaries representing role-based access control (RBAC) DefaultRolePermission definitions.
            grants (list): A list of dictionaries representing Grant definitions.
    Returns:
        dict: A dictionary containing structured information about entities, settings, and rules, organized for API consumption.
    """

    output = {}
    for r in root:
        output["about"] = {
            "date": r["about_date"],
            "recent_changes": r["about_changes"],
        }
        output["api_root"] = r["api_root"]
        output["authentication"] = {r["api_auth_type"]: r["api_auth"]}
        break

    entity_list = {}
    for entity in entities:
        entity_name = entity["name"]
        e = {}
        constraints = []
        events = []
        e["type"] = entity_name
        e["title"] = entity["title"]
        e["primary_key"] = convert_list(entity["pkey"])
        if entity.get("new_template"):
            e["new_template"] = entity["new_template"]
        if entity.get("home_template"):
            e["home_template"] = entity["home_template"]
        if entity.get("detail_template"):
            e["detail_template"] = entity["detail_template"]
        if entity.get("mode"):
            e["mode"] = entity["mode"]
        if entity.get("favorite"):
            e["favorite"] = entity.get("favorite")
        if entity.get("exclude"):
            e["exclude"] = entity["exclude"]
        else:
            e["exclude"] = False
        if entity.get("info_list"):
            e["info_list"] = entity["info_list"]
        if entity.get("info_show"):
            e["info_show"] = entity["info_show"]
        if entity.get("menu_group"):
            e["group"] = entity["menu_group"]
        for rule in rule_constraints:
            if rule["entity_name"] == entity_name:
                constraints.append(rule["rule"])
        for rule in rule_events:
            if rule["entity_name"] == entity_name:
                events.append(rule["rule"])
        if len(constraints) > 0 or len(events) > 0:
            e["rules"] = {"contraints": constraints, "events": events}

        entity_list[entity_name] = e

        cols = []
        for attr in attrs:
            col = {}
            if attr["entity_name"] == entity_name:
                col["name"] = attr["attr"]
                col["label"] = fixup(attr["label"])
                col["template"] = attr["template_name"]
                col["type"] = attr["thistype"]
                col["sort"] = attr.get("issort", False)
                col["search"] = attr.get("issearch", False)
                col["required"] = attr.get("isrequired", False)
                col["enabled"] = attr.get("isenabled", False)
                col["exclude"] = attr.get("exclude", False)
                col["visible"] = attr.get("visible", True)
                if attr.get("default_value"):
                    col["default_value"] = attr.get("default_value")
                if attr.get("derivation"):
                    col["derivation"] = attr.get("derivation")
                cols.append(col)
        entity_list[entity_name]["columns"] = cols
        tab_group = []
        for tab in tabs:
            tg = {}
            if tab["entity_name"] == entity_name:
                tg["direction"] = tab["direction"]
                tg["resource"] = tab["tab_entity"]
                tg["label"] = (
                    tab["label"] if tab.get("label") != None else tab.get("name")
                )
                tg["name"] = tab.get("name")
                tg["fks"] = convert_list(tab["fkeys"])
                tg["exclude"] = tab.get("exclude", False)
                tab_group.append(tg)
        if len(tab_group) > 0:
            entity_list[entity_name]["tab_groups"] = tab_group

    output["entities"] = entity_list

    output_yaml = {}
    output_yaml["entities"] = output
    style_guide = {}
    for s in settings:
        sg = {}

        name = s["name"]
        if name in ["use_keycloak", "include_translation"]:
            sg[name] = s["value"] == "1"
        else:
            sg[name] = s["value"]
        style_guide.update(sg)
        
    output["user_roles"] = {}
    output["user_roles"] = security_output["roles"]

    output["grants"] = {}
    output["grants"] = security_output["grants"]
    
    output["settings"] = {}
    output["settings"]["style_guide"] = style_guide

    return output


def fixup(label) -> str:
    label = label.replace("dlr_", "Dealer ")
    label = label.replace("img_", "Image ")
    label = label.replace("veh_", "Vehicle ")
    label = label.replace("inv_", "Invoice ")
    label = label.replace("user_", "User ")
    label = label.replace("_id", " Id")
    label = label.replace("_name", " Name")
    label = label.replace("_comment", " Comment")
    label = label.replace("_display", " Display")
    label = label.replace("_type", " Type")
    label = label.replace("_dt", " Date")
    label = label.replace("_", " ")
    s = label.split(" ")
    result = ""
    for t in s:
        if t != "":
            result += f"{t.capitalize()} "

    return result


def convert_list(key: str) -> list:
    k = key.replace("'", "", 20)
    k = k.replace("[", "")
    k = k.replace("]", "")
    l = []
    s = k.split(",")
    for v in s:
        l.append(v.strip())
    # return [v.strip() for v in s]
    return l


def getMetaData(resource_name: str = None, include_attributes: bool = True) -> dict:
    import inspect
    import sys
    import json

    resource_list = []  # array of attributes[], name (so, the name is last...)
    resource_objs = {}  # objects, named = resource_name

    models_name = "database.models"
    cls_members = inspect.getmembers(sys.modules["database.models"], inspect.isclass)
    for each_cls_member in cls_members:
        each_class_def_str = str(each_cls_member)
        if f"'{models_name}." in each_class_def_str and "Ab" not in each_class_def_str:
            each_resource_name = each_cls_member[0]
            each_resource_class = each_cls_member[1]
            each_resource_mapper = each_resource_class.__mapper__
            if resource_name is None or resource_name == each_resource_name:
                resource_object = {"name": each_resource_name}
                resource_list.append(resource_object)
                resource_objs[each_resource_name] = {}
                if include_attributes:
                    attr_list = []
                    for each_attr in each_resource_mapper.attrs:
                        if not each_attr._is_relationship:
                            try:
                                attribute_object = {
                                    "name": each_attr.key,
                                    "attr": each_attr,
                                    "type": str(each_attr.expression.type),
                                }
                            except Exception as ex:
                                attribute_object = {
                                    "name": each_attr.key,
                                    "exception": f"{ex}",
                                }
                            attr_list.append(attribute_object)
                    resource_object["attributes"] = attr_list
                    resource_objs[each_resource_name] = {
                        "attributes": attr_list,
                        "model": each_resource_class,
                    }
    # pick the format you like
    # return_result = {"resources": resource_list}
    return_result = {"resources": resource_objs}
    return return_result
