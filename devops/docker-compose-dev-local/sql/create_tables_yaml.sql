
DROP TABLE IF EXISTS entity;
DROP TABLE IF EXISTS entity_attr;
DROP TABLE IF EXISTS tab_group;
DROP TABLE IF EXISTS global_settings;
DROP TABLE IF EXISTS template;
DROP TABLE IF EXISTS root;

DROP TABLE IF EXISTS yaml_files;

DROP TABLE IF EXISTS rule_constraint;   

DROP TABLE IF EXISTS rule_event;

DROP TABLE IF EXISTS rule_derivation;

CREATE TABLE entity (
    name varchar(80) not null,
    title varchar(100) not null,
    pkey varchar(100),
    favorite varchar(100),
    info_list text,
    info_show text,
    exclude boolean default false,
    new_template VARCHAR(80), 
    home_template VARCHAR(80), 
    detail_template VARCHAR(80), 
    mode  VARCHAR(10) DEFAULT 'tab', menu_group VARCHAR(25), 
    PRIMARY KEY (name)
);


CREATE TABLE template (
    name varchar(100) not null,
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
    PRIMARY KEY (entity_name, attr),
    FOREIGN KEY (entity_name) REFERENCES entity(name),
    FOREIGN KEY (template_name) REFERENCES template(name)
);

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

CREATE TABLE yaml_files( 
    name VARCHAR(100) NOT NULL,    
    content TEXT,
    upload_flag BOOLEAN DEFAULT FALSE,
    download_flag    BOOLEAN DEFAULT FALSE, 
    size INT,
    downloaded text,
    rule_content TEXT,
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
    rule VARCHAR(255),
    FOREIGN KEY (entity_name) REFERENCES entity(name)
);

CREATE TABLE rule_event (  
    id SERIAL PRIMARY KEY,
    entity_name VARCHAR(80),
    event_type VARCHAR(25),
    calling_fn VARCHAR(255),
    rule VARCHAR(255),
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
    rule VARCHAR(255),
    insert_parent BOOLEAN,
    FOREIGN KEY (entity_name) REFERENCES entity(name),
    FOREIGN KEY (as_child_entity) REFERENCES entity(name)
);
