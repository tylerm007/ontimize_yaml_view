from sqlalchemy.ext.declarative import declarative_base
from safrs import SAFRSBase
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

@classmethod
def jsonapi_filter(cls):
    """
    Use this to override SAFRS JSON:API filtering

    Returns:
        _type_: SQLAlchemy query filter
    """
    from sqlalchemy import text, or_
    from flask import request
    expressions = []
    query = cls._s_query
    if args := request.args:
        from api.expression_parser import advancedFilter
        # Used by api_service layer  
        expressions = advancedFilter(cls, args)
        
    return query.filter(or_(*expressions))
    

class SAFRSBaseX(SAFRSBase):
    __abstract__ = True
    USE_ADVANCED_FILTER = False
    if USE_ADVANCED_FILTER:
        jsonapi_filter = jsonapi_filter

