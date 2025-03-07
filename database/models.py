# coding: utf-8
from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey, Integer, String, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  February 21, 2025 21:49:01
# Database: postgresql://postgres:postgres@127.0.0.1:5432/yaml
# Dialect:  postgresql
#
# mypy: ignore-errors
########################################################################################################################

from database.system.SAFRSBaseX import SAFRSBaseX, TestBase
from flask_login import UserMixin
import safrs, flask_sqlalchemy, os
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List
from sqlalchemy import Sequence

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.postgresql import *


Base = SAFRSBaseX 
class Application(Base):  # type: ignore
    __tablename__ = 'application'
    _s_collection_name = 'Application'  # type: ignore

    id = Column(BigInteger, Sequence('application_id_seq'), primary_key=True)
    name = Column(String(100), nullable=False)
    app_short_name = Column(String(100), server_default=text("app"))
    description = Column(Text)

    # parent relationships (access parent)

    # child relationships (access children)
    MenuGroupList : Mapped[List["MenuGroup"]] = relationship(back_populates="application")



class Entity(Base):  # type: ignore
    __tablename__ = 'entity'
    _s_collection_name = 'Entity'  # type: ignore

    name = Column(String(80), primary_key=True)
    title = Column(String(100), nullable=False)
    pkey = Column(String(100))
    favorite = Column(String(100))
    info_list = Column(Text)
    info_show = Column(Text)
    exclude = Column(Boolean, server_default=text("false"))
    new_template = Column(String(80))
    home_template = Column(String(80))
    detail_template = Column(String(80))
    mode = Column(String(10), server_default=text("tab"))
    menu_group = Column(String(25))
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)
    EntityAttrList : Mapped[List["EntityAttr"]] = relationship(back_populates="entity")
    GrantRoleList : Mapped[List["GrantRole"]] = relationship(back_populates="entity")
    RuleConstraintList : Mapped[List["RuleConstraint"]] = relationship(back_populates="entity")
    RuleDerivationList : Mapped[List["RuleDerivation"]] = relationship(foreign_keys='[RuleDerivation.as_child_entity]', back_populates="entity")
    RuleDerivationList1 : Mapped[List["RuleDerivation"]] = relationship(foreign_keys='[RuleDerivation.entity_name]', back_populates="entity1")
    RuleEventList : Mapped[List["RuleEvent"]] = relationship(back_populates="entity")
    TabGroupList : Mapped[List["TabGroup"]] = relationship(foreign_keys='[TabGroup.entity_name]', back_populates="entity")
    TabGroupList1 : Mapped[List["TabGroup"]] = relationship(foreign_keys='[TabGroup.tab_entity]', back_populates="entity1")
    MenuItemList : Mapped[List["MenuItem"]] = relationship(back_populates="entity")



class GlobalSetting(Base):  # type: ignore
    __tablename__ = 'global_settings'
    _s_collection_name = 'GlobalSetting'  # type: ignore

    name = Column(String(100), primary_key=True)
    value = Column(String(8000), nullable=False)
    description = Column(Text)
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)



class RbacRole(Base):  # type: ignore
    __tablename__ = 'rbac_role'
    _s_collection_name = 'RbacRole'  # type: ignore

    name = Column(String(80), primary_key=True)
    description = Column(Text)
    can_read = Column(Boolean, server_default=text("true"))
    can_insert = Column(Boolean, server_default=text("true"))
    can_update = Column(Boolean, server_default=text("true"))
    can_delete = Column(Boolean, server_default=text("true"))
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)
    GrantRoleList : Mapped[List["GrantRole"]] = relationship(back_populates="rbac_role")



class Root(Base):  # type: ignore
    __tablename__ = 'root'
    _s_collection_name = 'Root'  # type: ignore

    id = Column(Integer, primary_key=True)
    about_changes = Column(Text)
    api_root = Column(String(1000))
    api_auth_type = Column(String(100))
    api_auth = Column(String(1000))
    about_date = Column(String(100))
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)



class Template(Base):  # type: ignore
    __tablename__ = 'template'
    _s_collection_name = 'Template'  # type: ignore

    name = Column(String(100), primary_key=True)
    file_name = Column(String(100))
    description = Column(Text)
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)
    EntityAttrList : Mapped[List["EntityAttr"]] = relationship(back_populates="template")
    MenuItemList : Mapped[List["MenuItem"]] = relationship(back_populates="template")
    PageList : Mapped[List["Page"]] = relationship(back_populates="template")



class YamlFiles(Base):  # type: ignore
    __tablename__ = 'yaml_files'
    _s_collection_name = 'YamlFile'  # type: ignore

    name = Column(String(100), primary_key=True)
    content = Column(Text)
    upload_flag = Column(Boolean, server_default=text("false"))
    download_flag = Column(Boolean, server_default=text("false"))
    size = Column(Integer)
    file_path = Column(String(1000))
    app_name = Column(String(100))
    is_active = Column(Boolean, server_default=text("false"))
    downloaded = Column(Text)
    rule_content = Column(Text)
    role_content = Column(Text)
    local_storage = Column(Text)
    en_json = Column(Text)
    application_content = Column(Text)
    allow_client_generated_ids = True

    # parent relationships (access parent)

    # child relationships (access children)



class EntityAttr(Base):  # type: ignore
    __tablename__ = 'entity_attr'
    _s_collection_name = 'EntityAttr'  # type: ignore

    entity_name = Column(ForeignKey('entity.name'), primary_key=True, nullable=False)
    attr = Column(String(80), primary_key=True, nullable=False)
    label = Column(String(100))
    issearch = Column(Boolean, server_default=text("false"))
    issort = Column(Boolean, server_default=text("false"))
    thistype = Column(String(50), nullable=False)
    template_name = Column(ForeignKey('template.name'), server_default=text("text"))
    tooltip = Column(Text)
    isrequired = Column(Boolean, server_default=text("true"))
    isenabled = Column(Boolean, server_default=text("true"))
    exclude = Column(Boolean, server_default=text("false"))
    visible = Column(Boolean, server_default=text("true"))
    default_value = Column(String(100))
    derivation = Column(String(255))
    create_date = Column(DateTime, server_default=text("now()"))
    allow_client_generated_ids = True

    # parent relationships (access parent)
    entity : Mapped["Entity"] = relationship(back_populates=("EntityAttrList"))
    template : Mapped["Template"] = relationship(back_populates=("EntityAttrList"))

    # child relationships (access children)



class GrantRole(Base):  # type: ignore
    __tablename__ = 'grant_role'
    _s_collection_name = 'GrantRole'  # type: ignore

    entity_name = Column(ForeignKey('entity.name'), primary_key=True, nullable=False)
    role_name = Column(ForeignKey('rbac_role.name'), primary_key=True, nullable=False)
    can_read = Column(Boolean, server_default=text("true"))
    can_insert = Column(Boolean, server_default=text("false"))
    can_update = Column(Boolean, server_default=text("false"))
    can_delete = Column(Boolean, server_default=text("false"))
    filter = Column(Text)
    filter_debug = Column(Text)
    allow_client_generated_ids = True

    # parent relationships (access parent)
    entity : Mapped["Entity"] = relationship(back_populates=("GrantRoleList"))
    rbac_role : Mapped["RbacRole"] = relationship(back_populates=("GrantRoleList"))

    # child relationships (access children)



class MenuGroup(Base):  # type: ignore
    __tablename__ = 'menu_group'
    _s_collection_name = 'MenuGroup'  # type: ignore

    id = Column(BigInteger, Sequence('menu_group_id_seq'), primary_key=True)
    application_id = Column(ForeignKey('application.id', ondelete='CASCADE'), nullable=False)
    menu_name = Column(String(100), server_default=text("data"), nullable=False)
    menu_id = Column(String(100), server_default=text("data"))
    menu_title = Column(String(100))
    icon = Column(String(100), server_default=text("edit_square"))
    opened = Column(Boolean, server_default=text("false"))

    # parent relationships (access parent)
    application : Mapped["Application"] = relationship(back_populates=("MenuGroupList"))

    # child relationships (access children)
    MenuItemList : Mapped[List["MenuItem"]] = relationship(back_populates="menu_group")



class RuleConstraint(Base):  # type: ignore
    __tablename__ = 'rule_constraint'
    _s_collection_name = 'RuleConstraint'  # type: ignore

    id = Column(Integer, Sequence('rule_constraint_id_seq'), primary_key=True)
    entity_name = Column(ForeignKey('entity.name'))
    calling_fn = Column(String(255))
    as_condition = Column(String(255))
    err_msg = Column(String(255))
    error_attributes = Column(String(80))
    rule = Column(String(1000))

    # parent relationships (access parent)
    entity : Mapped["Entity"] = relationship(back_populates=("RuleConstraintList"))

    # child relationships (access children)



class RuleDerivation(Base):  # type: ignore
    __tablename__ = 'rule_derivation'
    _s_collection_name = 'RuleDerivation'  # type: ignore

    id = Column(Integer, Sequence('rule_derivation_id_seq'), primary_key=True)
    entity_name = Column(ForeignKey('entity.name'))
    derive_column = Column(String(80))
    expression = Column(String(255))
    derivation_type = Column(String(25))
    as_child_entity = Column(ForeignKey('entity.name'))
    child_role_name = Column(String(80))
    calling_fn = Column(String(80))
    where_clause = Column(String(255))
    rule = Column(String(1000))
    insert_parent = Column(Boolean)

    # parent relationships (access parent)
    entity : Mapped["Entity"] = relationship(foreign_keys='[RuleDerivation.as_child_entity]', back_populates=("RuleDerivationList"))
    entity1 : Mapped["Entity"] = relationship(foreign_keys='[RuleDerivation.entity_name]', back_populates=("RuleDerivationList1"))

    # child relationships (access children)



class RuleEvent(Base):  # type: ignore
    __tablename__ = 'rule_event'
    _s_collection_name = 'RuleEvent'  # type: ignore

    id = Column(Integer, Sequence('rule_event_id_seq'), primary_key=True)
    entity_name = Column(ForeignKey('entity.name'))
    event_type = Column(String(25))
    calling_fn = Column(String(255))
    rule = Column(String(1000))

    # parent relationships (access parent)
    entity : Mapped["Entity"] = relationship(back_populates=("RuleEventList"))

    # child relationships (access children)



class TabGroup(Base):  # type: ignore
    __tablename__ = 'tab_group'
    _s_collection_name = 'TabGroup'  # type: ignore

    entity_name = Column(ForeignKey('entity.name'), primary_key=True, nullable=False)
    tab_entity = Column(ForeignKey('entity.name'), primary_key=True, nullable=False)
    direction = Column(String(6), primary_key=True, nullable=False)
    fkeys = Column(String(80), nullable=False)
    name = Column(String(80), nullable=False)
    label = Column(String(80), primary_key=True, nullable=False)
    exclude = Column(Boolean, server_default=text("false"))
    allow_client_generated_ids = True

    # parent relationships (access parent)
    entity : Mapped["Entity"] = relationship(foreign_keys='[TabGroup.entity_name]', back_populates=("TabGroupList"))
    entity1 : Mapped["Entity"] = relationship(foreign_keys='[TabGroup.tab_entity]', back_populates=("TabGroupList1"))

    # child relationships (access children)



class MenuItem(Base):  # type: ignore
    __tablename__ = 'menu_item'
    _s_collection_name = 'MenuItem'  # type: ignore

    id = Column(BigInteger, Sequence('menu_item_id_seq', start=100), primary_key=True)
    menu_group_id = Column(ForeignKey('menu_group.id', ondelete='CASCADE'), nullable=False)
    entity_name = Column(ForeignKey('entity.name'), nullable=False)
    menu_name = Column(String(100), nullable=False)
    template_name = Column(ForeignKey('template.name'), server_default=text("module.jinja"))
    icon = Column(String(100), server_default=text("edit_square"))
    insert_page = Column("insert_pages", Boolean, server_default=text("true"))

    # parent relationships (access parent)
    entity : Mapped["Entity"] = relationship(back_populates=("MenuItemList"))
    menu_group : Mapped["MenuGroup"] = relationship(back_populates=("MenuItemList"))
    template : Mapped["Template"] = relationship(back_populates=("MenuItemList"))

    # child relationships (access children)
    PageList : Mapped[List["Page"]] = relationship(back_populates="menu_item")



class Page(Base):  # type: ignore
    __tablename__ = 'page'
    _s_collection_name = 'Page'  # type: ignore

    id = Column(BigInteger, Sequence('page_id_seq', start=100), primary_key=True)
    menu_item_id = Column(ForeignKey('menu_item.id', ondelete='CASCADE'), nullable=False)
    page_name = Column(String(10), nullable=False)
    title = Column(String(100))
    template_name = Column(ForeignKey('template.name'))
    typescript_name = Column(String(100))
    columns = Column(Text)
    visible_columns = Column(Text)
    include_children = Column(Boolean, server_default=text("true")) 


    # parent relationships (access parent)
    menu_item : Mapped["MenuItem"] = relationship(back_populates=("PageList"))
    template : Mapped["Template"] = relationship(back_populates=("PageList"))

    # child relationships (access children)
