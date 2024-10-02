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
#from api.gen_xlsx_report import xlsx_gen_report
import sqlite3
from os import path
import logging
import sys
from typing import Any, Optional, Tuple
from logic_bank.rule_bank.rule_bank import RuleBank

app_logger = logging.getLogger(__name__)

# This is the Ontimize Bridge API - all endpoints will be prefixed with /ontimizeweb/services/rest
# called by api_logic_server_run.py, to customize api (new end points, services).
# separate from expose_api_models.py, to simplify merge if project recreated
# version 11.x - api_logic_server_cli/prototypes/ont_app/prototype/api/api_discovery/ontimize_api.py

app_logger = logging.getLogger(__name__)

db = safrs.DB
session = db.session
_project_dir = None
app_logger.debug("api/api_discovery/rule_parser.py - services for ontimize")

class DotDict(dict):
    """dot.notation access to dictionary attributes"""

    # thanks: https://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary/28463329
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators=[]):
    _project_dir = project_dir
    pass

"""
Utilities for API Logic Server Projects (1.1)
"""

def log(msg: object) -> None:
    app_logger.debug(msg)
    # print("TIL==> " + msg)


def connection() -> sqlite3.Connection:
    ROOT: str = path.dirname(path.realpath(__file__))
    log(ROOT)
    _connection = sqlite3.connect(path.join(ROOT, "sqlitedata.db"))
    return _connection


def dbpath(dbname: str) -> str:
    ROOT: str = path.dirname(path.realpath(__file__))
    log('ROOT: '+ROOT)
    PATH: str = path.join(ROOT, dbname)
    log('DBPATH: '+PATH)
    return PATH

rule_count = 0
from flask import request, jsonify

def rules_report():
    """
    logs report of all rules, using rules_bank.__str__()
    """
    global rule_count
    rules_bank = RuleBank()
    logic_logger = logging.getLogger("logic_logger")
    rule_count = 0
    logic_logger.debug(f'\nThe following rules have been activated\n')
    list_rules = rules_bank.__str__()
    loaded_rules = list(list_rules.split("\n"))
    for each_rule in loaded_rules:
        logic_logger.info(each_rule + '\t\t##  ')
        rule_count += 1
    logic_logger.info(f'Logic Bank - {rule_count} rules loaded')

def get_rules(entity: str = None) -> dict:
    """
    {} report of all rules, using rules_bank.__str__()
    """
    rules_bank = RuleBank()
    rules_dict = {}
    rule_count = 0
    list_rules = rules_bank.__str__()
    loaded_rules = list(list_rules.split("\n"))
    for each_rule in loaded_rules:
        rules_dict[rule_count] = each_rule
        rule_count += 1
    return rules_dict

def get_rules_report(project_dir: str = None) -> any:
    rule_group = {}
    rule_type = {}
    for rule in get_rules_from_file(project_dir):
        entity = rule["entity"]
        type = rule["rule"].split("Rule.")[1].split("(")[0]
        if entity not in rule_group:
            rule_group[entity] = [rule["rule"]]
        else:
            rule_group[entity].append(rule["rule"])
        if type not in rule_type:
            rule_type[type] = [rule["rule"]]
        else:
            rule_type[type].append(rule["rule"])
    return rule_group, rule_type
            
def get_rules_from_content(content: str) -> list:
    rule_list = []
    results = []
    start = False
    count_left_parents, count_right_parents = 0, 0
    for line in content.split("\n"):
            this_line = clean(line)
            if this_line.startswith('Rule.'):
                rule_line = ""
                start = True
            if start:
                count_left_parents += this_line.count('(')
                count_right_parents += this_line.count(')')
                rule_line += this_line
            if count_left_parents == count_right_parents and start:
                rule_list.append(rule_line.strip())
                start = False
                rule_line = ""
                count_left_parents, count_right_parents = 0, 0
    
    for rule in rule_list:
        print(rule)
        type = rule.split("Rule.")[1].split("(")[0]
        if type == "early_row_event_all_classes":
            entity = "all"
        else:
            entity = rule.split("Rule.")[1].split("(")[1].split(",")[0].split(".")[1]

        row = {"type": type, "entity": entity, "rule": rule, "attr": parse_rule_for_attr(rule, type)}
        
        results.append(row)
        
    return results

def parse_rule_for_attr(rule: str, type: str) -> str:
    if type == "constraint" or type.endswith("_event"):
        return None
    return rule.split("Rule.")[1].split("(")[1].split(",")[0].split(".")[-1]
def get_rules_from_file(project_dir: str = None) -> list:
    rule_list = parse_rules(project_dir)
    results = []
    for rule in rule_list:
        print(rule)
        type = rule.split("Rule.")[1].split("(")[0]
        if type == "early_row_event_all_classes":
            entity = "all"
        else:
            entity = rule.split("Rule.")[1].split("(")[1].split(",")[0].split(".")[1]
        row = {"type": type, "entity": entity, "rule": rule}
        results.append(row)
        
    return results
        
    
def parse_rules(project_dir: str = None) -> list:
    result = []
    rule_line = ""
    count_left_parents, count_right_parents = 0, 0
    with open(f'{project_dir}/logic/declare_logic.py', 'r') as f:
        start = False
        for line in f:
            this_line = clean(line)
            if this_line.startswith('Rule.'):
                rule_line = ""
                start = True
            if start:
                count_left_parents += this_line.count('(')
                count_right_parents += this_line.count(')')
                rule_line += this_line
            if count_left_parents == count_right_parents and start:
                result.append(rule_line)
                start = False
                rule_line = ""
                count_left_parents, count_right_parents = 0, 0
    return result
                
def clean(line) -> str:
    # strip comments and empty lines or comment lines
    l = line.strip()    
    if l and len(l) > 1 and l[0] == "#":
        return ""
    if l and len(l) > 6 and l.find("#") > 0:
        return l[:l.find("#")]
    return l
def server_log(request, jsonify):
    """
    Used by test/*.py - enables client apps (the behave tests) to...
    *  log msg into server, and 
    * test/api_logic_server_behave/logs
    """
    import os
    import datetime
    from pathlib import Path
    import logging
    global rule_count


    def add_file_handler(logger, name: str, log_dir):
        """Add a file handler for this logger with the specified `name` (and
        store the log file under `log_dir`)."""
        # Format for file log
        for each_handler in logger.handlers:
            each_handler.flush()
            handler_name = str(each_handler)
            if "stderr" in handler_name:
                pass
                # print(f'do not delete stderr')
            else:
                logger.removeHandler(each_handler)
        fmt = '%(asctime)s | %(levelname)8s | %(filename)s:%(lineno)d | %(message)s'
        formatter = logging.Formatter(fmt)
        formatter = logging.Formatter('%(message)s - %(asctime)s - %(name)s - %(levelname)s')

        # Determine log path/file name; create log_dir if necessary
        now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        log_name = f'{str(name).replace(" ", "_")}'  # {now}'
        if len(log_name) >= 26:
            log_name = log_name[0:25]

        if not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir)
            except:
                app_logger.info(f'util.add_file_handler unable to create dir {log_dir}')
                log_dir = '/tmp' if sys.platform.startswith('linux') else '.'
                app_logger.info(f'Defaulting to {log_dir}.')

        log_file = os.path.join(log_dir, log_name) + '.log'
        if os.path.exists(log_file):
            os.remove(log_file)
        else:
            pass  # file does not exist

        # Create file handler for logging to a file (log all five levels)
        # print(f'create file handler for logging: {log_file}')
        logger.file_handler = logging.FileHandler(log_file)
        logger.file_handler.setLevel(logging.DEBUG)
        logger.file_handler.setFormatter(formatter)
        logger.addHandler(logger.file_handler)

    msg = request.args.get('msg')
    test = request.args.get('test')
    if "Server Log: Behave Run Successfully Completed" in msg:
        debug_stop = 'good breakpoint'
    if test is not None and test != "None":
        if test == "None":
            print(f'None for msg: {msg}')
        logic_logger = logging.getLogger('logic_logger')  # for debugging user logic
        # logic_logger.info("\n\nLOGIC LOGGER HERE\n")
        use_relative = True
        if use_relative:
            api_utils_path = Path(__file__)
            proj_path = api_utils_path.parent.parent.parent
            log_path = proj_path.joinpath('test/api_logic_server_behave/logs/scenario_logic_logs')
            print(f'Log Dir: {log_path}')
            add_file_handler(logic_logger, test, log_path)
        else:
            dir = request.args.get('dir')
            add_file_handler(logic_logger, test, Path(os.getcwd()).joinpath(dir))
    if msg == "Rules Report":
        rules_report()
        logic_logger.info(f'Logic Bank - {rule_count} rules loaded')
    else:
        app_logger.info(f'{msg}')
        if "Server Log: Behave Run Successfully Completed" in msg:
            logic_logger.info(f'\n\n*** {msg}\n\n***\n\n')
    return jsonify({"result": f'ok'})


def sys_info(flask_app_config):  
    """
    Print env and path
    """  
    import os, socket
    print("\n\nsys_info here")
    print("\nEnvironment Variables...")
    env = os.environ
    for each_variable in os.environ:
            print(f'.. {each_variable} = {env[each_variable]}')

    print(f'\n\nflask_app.config: \n\t')
    flask_app_config_str = str(flask_app_config)
    flask_app_config_str = flask_app_config_str.replace(', ', ',\n\t')
    print((flask_app_config_str))

    print("\n\nPYTHONPATH..")
    for p in sys.path:
        print(".." + p)
        
    print("")
    print(f'sys.prefix (venv): {sys.prefix}\n')

    print("")
    hostname = socket.gethostname()
    IPAddr = 'unknown'
    try:
        local_ip = socket.gethostbyname(hostname)
        IPAddr=socket.gethostbyname(hostname) 
    except:
        local_ip = f"Warning - Failed local_ip = socket.gethostbyname(hostname) with hostname: {hostname}"

    print(f"hostname={hostname} on local_ip={local_ip}, IPAddr={IPAddr}\n\n")

    print(f"os.getcwd()={os.getcwd()}\n\n")