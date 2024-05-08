"""
Advanced Expression Parsing - return SQL Where clause
"""
import json
BASIC_EXPRESSION = "@basic_expression"
FILTER_EXPRESSION = "@filter_expression"
LESS = "<"
LESS_EQUAL = "<="
EQUAL = "="
MORE_EQUAL = ">="
MORE = ">"
NULL = " IS NULL "
NOT_EQUAL = "<>"
NOT_NULL = " IS NOT NULL "
LIKE = " LIKE "
NOT_LIKE = " NOT LIKE "
OR = " OR "
AND = " AND "
OR_NOT = " OR NOT "
AND_NOT = " AND NOT "
class DotDict(dict):
    """ dot.notation access to dictionary attributes """
    # thanks: https://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary/28463329
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

def parsePayload(payload:str):
    """
        employee/advancedSearch
        {"filter":{},"columns":["EMPLOYEEID","EMPLOYEETYPEID","EMPLOYEENAME","EMPLOYEESURNAME","EMPLOYEEADDRESS","EMPLOYEESTARTDATE","EMPLOYEEEMAIL","OFFICEID","EMPLOYEEPHOTO","EMPLOYEEPHONE"],"sqltypes":{},"offset":0,"pageSize":16,"orderBy":[]}
        customers/customer/advancedSearch
        {"filter":{},"columns":["CUSTOMERID","NAME","SURNAME","ADDRESS","STARTDATE","EMAIL"],"sqltypes":{"STARTDATE":93},"offset":0,"pageSize":25,"orderBy":[{"columnName":"SURNAME","ascendent":true}]}
        
    """
    sqltypes = payload.get('sqltypes') or None
    _filter = parseFilter(payload.get('filter', {}),sqltypes)
    columns:list = payload.get('columns') or []
    offset:int = payload.get('offset') or 0
    pagesize:int = payload.get('pageSize') or 75
    orderBy:list = payload.get('orderBy') or []
    data = payload.get('data',None)
    
    print(_filter, columns, sqltypes, offset, pagesize, orderBy, data)
    return _filter, columns, sqltypes, offset, pagesize, orderBy, data

def parseFilter(filter:dict,sqltypes: any):
    # {filter":{"@basic_expression":{"lop":"BALANCE","op":"<=","rop":35000}}
    filter_result = ""
    a = ""
    for f in filter:
        value = filter[f]
        q = "'" 
        if f == BASIC_EXPRESSION:
            #{'lop': 'CustomerId', 'op': 'LIKE', 'rop': '%A%'}}
            if'lop' in value.keys() and 'rop' in value.keys():
                lop = value["lop"]
                op  = value["op"]
                rop  = f"{q}{value['rop']}{q}"
                filter_result = f'"{lop}" {op} {rop}'
                return filter_result
        if sqltypes == None:
            q = "'"
        else:
            q = "" if hasattr(sqltypes,f) and sqltypes[f] != 12 else "'"
        if f == "CategoryName":
            f = "CategoryName_ColumnName" #hack to use real column name
        filter_result += f'{a} "{f}" = {q}{value}{q}'
        a = " and "
    return None if filter_result == "" else filter_result


class BasicExpression():
    def __init__(self, lop: any = None, op: str = None, rop: any = None):
        self.lop_ext = []
        self.rop_ext= []
        
        self.lop = lop
        self.op = op
        self.rop = rop
        self.sql_where = "" 
        
        if isinstance(lop, dict):
            _lop = lop['lop']
            _op = lop['lop']['op'] if hasattr(lop,'op') else lop['op']
            _rop = lop['lop']['rop'] if hasattr(lop,'rop') else lop['rop']
            self.lop_ext.append(BasicExpression(_lop,_op,_rop))
        if isinstance(rop,dict):
            _lop = rop['lop']
            _op = rop['lop']['op'] if hasattr(rop,'op') else rop['op']
            _rop = rop['lop']['rop'] if hasattr(rop,'rop') else rop['rop']
            self.rop_ext.append(BasicExpression(_lop,_op,_rop))
    
    def get_sql_where(self):
        self.where(self)
        return self.sql_where
    def where(self, expr):
        if isinstance(expr, BasicExpression):
            for row in expr.lop_ext:
                self.where(row)
            for row in expr.rop_ext:
                self.where(row)
        '''
        if isinstance(expr.lop, dict):
            self.where(expr.lop)
        if isinstance(expr.rop, dict):
            self.where(expr.rop)
        '''
        if isinstance(expr.lop, str) and not isinstance(expr.rop, dict):
            self.sql_where += self._parseExpression(" AND ",expr=expr)
    
    
    def _parseExpression(self,op, expr) -> str:
        if expr.op != None and expr.rop != None:
            q = "" if expr.is_numeric(expr.rop) else "'"
            return f'"{op} {expr.lop}" {expr.op} {q}{expr.rop}{q}'
        return ""
    def is_numeric(self, value):
        return False
class ExpressionParser():
    
    def __init__(self, filter):
        self.filter = filter
        self.basic_expr = None
        f = self.parse(filter)
        self.build_sql_where(f)

    def get_expr(self):
        #return self.build_sql_where(self.basic_expr) if self.basic_expr else "1=1"
        self.build_sql_where(self.basic_expr)
    def parse(self, filter):
        return next((filter[f] for f in filter if f == BASIC_EXPRESSION), None)
    
    def get_sql_where(self):
        return self.basic_expr.get_sql_where()
    
    def build_sql_where(self, expr):
        print(expr)
        lop = expr["lop"]
        op = expr["op"]
        rop =expr["rop"] 
        self.basic_expr = BasicExpression(lop,op,rop)


        

if __name__ == '__main__':
    filter = '''
        {"filter": {
            "@basic_expression": {
                "lop": {
                    "lop": {
                        "lop": {
                            "lop": {
                                "lop": {
                                    "lop": "EMPLOYEENAME",
                                    "op": "LIKE",
                                    "rop": "%empname%"
                                },
                                "op": "OR",
                                "rop": {
                                    "lop": "EMPLOYEESURNAME",
                                    "op": "LIKE",
                                    "rop": "%surname%"
                                }
                            },
                            "op": "OR",
                            "rop": {
                                "lop": "EMPLOYEEADDRESS",
                                "op": "LIKE",
                                "rop": "%address%"
                            }
                        },
                        "op": "OR",
                        "rop": {
                            "lop": "EMPLOYEEEMAIL",
                            "op": "LIKE",
                            "rop": "%email%"
                        }
                    },
                    "op": "OR",
                    "rop": {
                        "lop": "OFFICEID",
                        "op": "LIKE",
                        "rop": "%officeid%"
                    }
                },
                "op": "AND",
                "rop": {
                    "lop": "EMPLOYEENAME",
                    "op": "LIKE",
                    "rop": "%pamella%"
                }
            }
        },
        "columns": [
            "EMPLOYEEID",
            "EMPLOYEETYPEID",
            "EMPLOYEENAME",
            "EMPLOYEESURNAME",
            "EMPLOYEEADDRESS",
            "EMPLOYEESTARTDATE",
            "EMPLOYEEEMAIL",
            "OFFICEID",
            "EMPLOYEEPHOTO",
            "EMPLOYEEPHONE",
            "NAME"
        ],
        "sqltypes": {},
        "offset": 0,
        "pageSize": 16,
        "orderBy": []
    }
    '''
    #'filter': {'@basic_expression': {'lop': {'lop': {'lop': {'lop': {'lop': {'lop': 'EMPLOYEENAME', 'op': 'LIKE', 'rop': '%fort%'}, 'op': 'OR', 'rop': {'lop': 'EMPLOYEESURNAME', 'op': 'LIKE', 'rop': '%fort%'}}, 'op': 'OR', 'rop': {'lop': 'EMPLOYEEADDRESS', 'op': 'LIKE', 'rop': '%fort%'}}, 'op': 'OR', 'rop': {'lop': 'EMPLOYEEEMAIL', 'op': 'LIKE', 'rop': '%fort%'}}, 'op': 'OR', 'rop': {'lop': 'OFFICEID', 'op': 'LIKE', 'rop': '%fort%'}}, 'op': 'AND', 'rop': {'lop': 'EMPLOYEENAME', 'op': 'LIKE', 'rop': '%pamella%'}}}, 'columns': ['EMPLOYEEID', 'EMPLOYEETYPEID', 'EMPLOYEENAME', 'EMPLOYEESURNAME', 'EMPLOYEEADDRESS', 'EMPLOYEESTARTDATE', 'EMPLOYEEEMAIL', 'OFFICEID', 'EMPLOYEEPHOTO', 'EMPLOYEEPHONE', 'NAME'], 'sqltypes': {}, 'offset': 0, 'pageSize': 16, 'orderBy': []}
    simple = {"filter":{"@basic_expression":{"lop":"BALANCE","op":"<=","rop":35000}}}
    fltr = json.loads(filter)
    ep = ExpressionParser(fltr["filter"])
    #ep = ExpressionParser(simple["filter"])
    print(ep.get_sql_where())