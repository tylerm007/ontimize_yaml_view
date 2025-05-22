import datetime, os
from decimal import Decimal
from logic_bank.exec_row_logic.logic_row import LogicRow
from logic_bank.extensions.rule_extensions import RuleExtension
from logic_bank.logic_bank import Rule
from logic_bank.logic_bank import DeclareRule
import database.models as models
import api.system.opt_locking.opt_locking as opt_locking
from security.system.authorization import Grant, Security
from logic.load_verify_rules import load_verify_rules
import integration.kafka.kafka_producer as kafka_producer
import logging
from base64 import b64decode
from requests import get, post
import yaml
from database.models import YamlFiles
from api.api_discovery.ontimize_api import insert_page
from uuid import uuid4

app_logger = logging.getLogger(__name__)
encoding = 'utf-8'
declare_logic_message = "ALERT:  *** No Rules Yet ***"  # printed in api_logic_server.py

def declare_logic():
    ''' Declarative multi-table derivations and constraints, extensible with Python.
 
    Brief background: see readme_declare_logic.md
    
    Your Code Goes Here - Use code completion (Rule.) to declare rules
    '''

    if os.environ.get("WG_PROJECT"):
        # Inside WG: Load rules from docs/expprt/export.json
        load_verify_rules()
    else:
        # Outside WG: load declare_logic function
        from logic.logic_discovery.auto_discovery import discover_logic
        discover_logic()

    def handle_all(logic_row: LogicRow):  # #als: TIME / DATE STAMPING, OPTIMISTIC LOCKING
        """
        This is generic - executed for all classes.

        Invokes optimistic locking.

        You can optionally do time and date stamping here, as shown below.

        Args:
            logic_row (LogicRow): from LogicBank - old/new row, state
        """
        if logic_row.is_updated() and logic_row.old_row is not None and logic_row.nest_level == 0:
            opt_locking.opt_lock_patch(logic_row=logic_row)
        enable_creation_stamping = True  # CreatedOn time stamping
        if enable_creation_stamping:
            row = logic_row.row
            if logic_row.ins_upd_dlt == "ins" and hasattr(row, "createdate"):
                #row.createdate = datetime.datetime.now()
                logic_row.log("early_row_event_all_classes - handle_all sets 'createdate"'')
        
        Grant.process_updates(logic_row=logic_row)

    Rule.early_row_event_all_classes(early_row_event_all_classes=handle_all) 
    def insert_pages(row: models.MenuItem, old_row: models.MenuItem, logic_row: LogicRow):
        if logic_row.ins_upd_dlt == "ins" and  row.insert_page == True:
            col_list = []
            menu_item_id = row.id
            attrs = logic_row._get_parent_logic_row('entity').row.EntityAttrList
            for col in attrs:
                col_list.append(col.attr)
            for page_name in ['new', 'home', 'detail']: 
                insert_page(page_name, col_list, row.entity_name, menu_item_id)
                
    Rule.after_flush_row_event(models.MenuItem, calling=insert_pages)          
    def validate_yaml(row: YamlFiles, old_row: YamlFiles, logic_row:LogicRow):
        if logic_row.ins_upd_dlt in ["ins"]:# and (row.download_flag is None or row.download_flag == False):
            if row.content:
                yaml_content = str(b64decode(row.content), encoding=encoding) if row.content else None 
                try:
                    ont_yaml = yaml.safe_load(yaml_content)
                    if ont_yaml.get('entities') is None:
                        app_logger.debug("The yaml file must be a valid app_model.yaml file")
                        return False
                    ont_yaml['project_name'] = row.name
                    row.size = len(ont_yaml)
                    row.upload_flag = False
                    row.download_flag = False
                    row.content = yaml.safe_dump(ont_yaml, default_flow_style=False, sort_keys=True)
                except yaml.YAMLError as exc:
                    app_logger.debug("The yaml file must be a valid app_model.yaml file")
                    row.content = None
                    return False
                
            if row.rule_content:  
                row.rule_content = str(b64decode(row.rule_content), encoding=encoding) if row.rule_content else None
            if row.role_content:
                row.role_content = str(b64decode(row.role_content), encoding=encoding) if row.role_content else None    
            if row.local_storage:
                row.local_storage = str(b64decode(row.local_storage), encoding=encoding) if row.local_storage else None    
        return True
    
    def initialize_new_project(row: YamlFiles, old_row: YamlFiles, logic_row: LogicRow):
        from pathlib import Path            
        running_at = Path(__file__) 
        project_dir = running_at.parent.parent
        from api.api_discovery.ontimize_api import initialize_project
        if logic_row.ins_upd_dlt == "ins":
            initialize_project(project_dir, row.file_path, row.content, row.rule_content, row.role_content)
            
    def create_application(row: YamlFiles, old_row: YamlFiles, logic_row: LogicRow):
        #from api.api_discovery.ontimize_api import insert_application
        #if logic_row.is_updated and row.file_path != old_row.file_path: 
        #    insert_application()
        pass
    
    def export_yaml(row: YamlFiles, old_row: YamlFiles, logic_row:LogicRow):
        if logic_row.is_updated and row.download_flag and old_row.download_flag == False and row.content != None:
            from api.api_discovery.ontimize_api import export_yaml_to_file
            from pathlib import Path
            running_at = Path(__file__) 
            project_dir = running_at.parent.parent
            #row.downloaded = export_yaml_to_file(project_dir=project_dir)
                
    Rule.row_event(YamlFiles, calling=export_yaml)
    #Rule.row_event(YamlFiles,calling=create_application)
    Rule.constraint(YamlFiles, calling=validate_yaml, error_msg="Invalid app_model.yaml file")
    #Rule.row_event(on_class=models.RuleDerivation, calling=parse_derivation_rule)

    Rule.formula(models.Application.project_uuid, as_expression=lambda row: str(row.yaml_files.file_path) if row.yaml_files.file_path else str(uuid4()))
    Rule.after_flush_row_event(models.YamlFiles, calling=initialize_new_project)
    app_logger.debug("..logic/declare_logic.py (logic == rules + code)")

