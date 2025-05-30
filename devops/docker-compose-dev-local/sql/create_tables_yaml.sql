

DROP TABLE IF EXISTS entity_attr;
DROP TABLE IF EXISTS tab_group;
DROP TABLE IF EXISTS global_settings;
DROP TABLE IF EXISTS template;
DROP TABLE IF EXISTS root;
DROP TABLE IF EXISTS rule_constraint;
DROP TABLE IF EXISTS rule_event;
DROP TABLE IF EXISTS rule_derivation;
DROP TABLE IF EXISTS grant_role;
DROP TABLE IF EXISTS rbac_role;
DROP TABLE IF EXISTS page_properties;
DROP TABLE IF EXISTS page;
DROP TABLE IF EXISTS menu_item;
DROP TABLE IF EXISTS menu_group;
DROP TABLE IF EXISTS application;
DROP TABLE IF EXISTS entity;
DROP TABLE IF EXISTS yaml_files;

CREATE TABLE entity (
    name varchar(80) not null,
    title varchar(100) not null,
    pkey varchar(100),
    favorite varchar(100),
    info_list text,
    info_show text,
    exclude boolean default false,
    -- new_template VARCHAR(80), 
    -- home_template VARCHAR(80), 
    -- detail_template VARCHAR(80), 
    mcp_enabled boolean default true,
    mcp_get boolean default true,
    mcp_post boolean default true,
    mcp_delete boolean default false,
    mcp_patch boolean default false,
    mode  VARCHAR(10) DEFAULT 'tab', menu_group VARCHAR(25), 
    PRIMARY KEY (name)
);


CREATE TABLE template (
    name varchar(100) not null,
    file_name varchar(100),
    description text,
    PRIMARY KEY (name)
);


CREATE TABLE entity_attr (
    entity_name varchar(80) not null,
    attr varchar(80) not null,
    label varchar(100),
    issearch boolean default false,
    issort boolean default false,
    thistype varchar(50) not null,
    template_name varchar(100) default 'text',
    tooltip text,
    isrequired boolean default true,
    isenabled boolean default true,
    exclude boolean default false,
    visible boolean default true, default_value VARCHAR(100),
    derivation VARCHAR(255),
    create_date TIMESTAMP default now(),
    PRIMARY KEY (entity_name, attr),
    FOREIGN KEY (entity_name) REFERENCES entity(name),
    FOREIGN KEY (template_name) REFERENCES template(name)
);

-- Relationship between parent and child entities
CREATE TABLE tab_group (
    entity_name varchar(80) not null,
    tab_entity varchar(80) not null,
    direction varchar(6) not null,
    fkeys varchar(80) not null,
    name varchar(80) not null,
    label varchar(80) not null,
    exclude boolean default false,
    PRIMARY KEY (entity_name,tab_entity,direction, label),
    FOREIGN KEY (entity_name) REFERENCES entity(name),
    FOREIGN KEY (tab_entity) REFERENCES entity(name)
    
);
-- moving away from storing contents and pushing to local directory
CREATE TABLE yaml_files( 
    name VARCHAR(100) NOT NULL,    
    content TEXT,
    upload_flag BOOLEAN DEFAULT FALSE,
    download_flag    BOOLEAN DEFAULT FALSE, 
    size INT,
    file_path VARCHAR(1000),
    app_name VARCHAR(100),
    is_active BOOLEAN default false,
    downloaded text,
    rule_content TEXT,
    role_content TEXT,
    local_storage TEXT,
    en_json TEXT,
    application_content TEXT,
    PRIMARY KEY(name)
);

CREATE TABLE root (
    id INTEGER NOT NULL,
    about_changes TEXT,
    api_root VARCHAR(1000),
    api_auth_type VARCHAR(100),
    api_auth VARCHAR(1000),
    about_date VARCHAR(100),
    PRIMARY KEY(id)
);

CREATE TABLE global_settings (
    name varchar(100) not null,
    value varchar(8000) not null,
    description text,
    PRIMARY KEY (name)
);

CREATE TABLE rule_constraint (  
    id SERIAL PRIMARY KEY,
    entity_name VARCHAR(80),
    calling_fn VARCHAR(255),
    as_condition VARCHAR(255),
    err_msg VARCHAR(255),
    error_attributes VARCHAR(80),
    rule TEXT,
    FOREIGN KEY (entity_name) REFERENCES entity(name)
);

CREATE TABLE rule_event (  
    id SERIAL PRIMARY KEY,
    entity_name VARCHAR(80),
    event_type VARCHAR(25),
    calling_fn VARCHAR(255),
    rule TEXT,
    FOREIGN KEY (entity_name) REFERENCES entity(name)
);

CREATE TABLE rule_derivation (  
    id SERIAL PRIMARY KEY,
    entity_name VARCHAR(80),
    derive_column VARCHAR(80),
    expression VARCHAR(255),
    derivation_type VARCHAR(25),
    as_child_entity VARCHAR(80),
    child_role_name VARCHAR(80),
    calling_fn VARCHAR(80),
    where_clause VARCHAR(255),
    rule TEXT,
    insert_parent BOOLEAN,
    FOREIGN KEY (entity_name) REFERENCES entity(name),
    FOREIGN KEY (as_child_entity) REFERENCES entity(name)
);


CREATE TABLE rbac_role (
    name varchar(80) not null,
    description TEXT,
    can_read BOOLEAN DEFAULT TRUE,
    can_insert  BOOLEAN DEFAULT TRUE,
    can_update  BOOLEAN DEFAULT TRUE,
    can_delete BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (name)
);

CREATE TABLE grant_role (
    entity_name varchar(80) not null,
    role_name varchar(80) not null,
    can_read BOOLEAN DEFAULT TRUE,
    can_insert  BOOLEAN DEFAULT FALSE,
    can_update  BOOLEAN DEFAULT FALSE,
    can_delete BOOLEAN DEFAULT FALSE,
    filter TEXT,
    filter_debug TEXT,
    PRIMARY KEY (entity_name, role_name),
    FOREIGN KEY (entity_name) REFERENCES entity(name),
    FOREIGN KEY (role_name) REFERENCES rbac_role(name)
);

CREATE TABLE application (
    id SERIAL8 NOT NULL,
    name VARCHAR(100) NOT NULL,
    app_short_name VARCHAR(100) DEFAULT 'app',
    api_root VARCHAR(1000) NOT NULL DEFAULT 'http://localhost:5656/api',
    description TEXT,
    yaml_name VARCHAR(100) NOT NULL,
    project_uuid VARCHAR(100),
    FOREIGN KEY (yaml_name) REFERENCES yaml_files(name),
    PRIMARY KEY(id)
);

CREATE TABLE menu_group (
    id SERIAL8 NOT NULL,  
    application_id BIGINT NOT NULL,
    menu_id VARCHAR(100) NOT NULL DEFAULT 'data',
    menu_name VARCHAR(100) DEFAULT 'data',
    menu_title VARCHAR(100),
    icon VARCHAR(100) DEFAULT 'edit_square',
    opened BOOLEAN DEFAULT FALSE,
    PRIMARY KEY(id),
    FOREIGN KEY (application_id) REFERENCES application(id) ON DELETE CASCADE
);

CREATE TABLE menu_item (
    id SERIAL8 NOT NULL,
    menu_group_id BIGINT NOT NULL,
    entity_name VARCHAR(100) NOT NULL, -- API Entity Name
    menu_name VARCHAR(100) NOT NULL,  -- Menu Item Name
    template_name VARCHAR(100) DEFAULT 'module.jinja',
    icon VARCHAR(100) DEFAULT 'edit_square',
    insert_pages BOOLEAN DEFAULT TRUE, -- internal used by rules
    PRIMARY KEY(id),
    FOREIGN KEY (entity_name) REFERENCES entity(name),
    FOREIGN KEY (menu_group_id) REFERENCES menu_group(id) ON DELETE CASCADE
);

CREATE TABLE page (
    id SERIAL8 NOT NULL,
    menu_item_id BIGINT NOT NULL,
    page_name VARCHAR(10) NOT NULL, -- home, new, detail
    title VARCHAR(100),
    template_name VARCHAR(100),
    typescript_name VARCHAR(100),
    columns VARCHAR(1000),
    visible_columns VARCHAR(1000),
    include_children BOOLEAN DEFAULT TRUE,
    PRIMARY KEY(id),
    FOREIGN KEY (menu_item_id) REFERENCES menu_item(id) ON DELETE CASCADE
);

CREATE TABLE page_properties (
    id SERIAL8 NOT NULL,
    page_id BIGINT NOT NULL,
    property_name VARCHAR(100) NOT NULL,
    property_value VARCHAR(1000),
    property_type VARCHAR(100),  --string, number, boolean, date
    PRIMARY KEY(id),
    FOREIGN KEY (page_id) REFERENCES page(id) ON DELETE CASCADE
);