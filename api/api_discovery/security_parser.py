import logging

app_logger = logging.getLogger(__name__)

# This is the Ontimize Bridge API - all endpoints will be prefixed with /ontimizeweb/services/rest
# called by api_logic_server_run.py, to customize api (new end points, services).
# separate from expose_api_models.py, to simplify merge if project recreated
# version 11.x - api_logic_server_cli/prototypes/ont_app/prototype/api/api_discovery/ontimize_api.py

app_logger = logging.getLogger(__name__)

_project_dir = None
app_logger.debug("api/api_discovery/security_parser.py - services for ontimize")


class DotDict(dict):
    """dot.notation access to dictionary attributes"""

    # thanks: https://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary/28463329
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def add_service(
    app, api, project_dir, swagger_host: str, PORT: str, method_decorators=[]
):
    _project_dir = project_dir
    pass


def parse_file(role_content: str = None , security_type: str = "DefaultRolePermission(") -> list:
    result = []
    rule_line = ""
    count_left_parents, count_right_parents = 0, 0
    if role_content:
        f = role_content.split("\n")
        start = False
        for line in f:
            this_line = clean(line)
            if this_line.startswith(security_type):
                rule_line = ""
                start = True
            if start:
                count_left_parents += this_line.count("(")
                count_right_parents += this_line.count(")")
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
        return l[: l.find("#")]
    return l


def get_security(role_content: str = None) -> list:
    rbac_list = parse_file(role_content,"DefaultRolePermission(")
    results = []
    for rbac in rbac_list:
        print(rbac)
        rb = rbac.strip().replace(")", "").split("DefaultRolePermission(")[1].split(",")
        row = {"can_read": False, "can_insert": False, "can_update": False, "can_delete": False, "to_role": ""}
        for r in rb:
            s1 = r.replace(" ", "", 4).split("=")
            if s1[0] == "can_read":
                row["can_read"] = s1[1] == "True"
            if s1[0] == "can_insert":
                row["can_insert"] = s1[1] == "True"
            if s1[0] == "can_update":
                row["can_update"] = s1[1] == "True"
            if s1[0] == "can_delete":
                row["can_delete"] = s1[1] == "True"
            if s1[0] == "to_role":
                row["to_role"] = s1[1].replace("'", "", 2).replace("Roles.","")

        results.append(row)

    return results
def get_grants(role_content: str = None) -> list:
    rbac_list = parse_file(role_content, "Grant(")
    results = []
    for rbac in rbac_list:
        print(rbac)
        rb = rbac.strip().replace(")", "").split("Grant(")[1].split(",")
        row = {"can_read": False, "can_insert": False, "can_update": False, "can_delete": False, "to_role": "", "on_entity": "", "filter": "","filter_debug":""}
        for r in rb:
            s1 = r.replace(" ", "", 4).split("=")
            if s1[0] == "can_read":
                row["can_read"] = s1[1] == "True"
            if s1[0] == "can_insert":
                row["can_insert"] = s1[1] == "True"
            if s1[0] == "can_update":
                row["can_update"] = s1[1] == "True"
            if s1[0] == "can_delete":
                row["can_delete"] = s1[1] == "True"
            if s1[0] == "to_role":
                row["to_role"] = s1[1].replace("'", "", 2).replace("Roles.","")
            if s1[0] == "on_entity":
                row["on_entity"] = s1[1].replace("'", "", 2).replace("models.", "")
            if s1[0] == "filter":
                s = rbac.split("filter=")
                row["filter"] = s[1].replace("'", "", 2)[:-1]
            if s1[0] == "filter_debug":
                s = rbac.split("filter_debug=")
                row["filter_debug"] = s[1].replace("'", "", 2)[:-1]

        results.append(row)

    return results