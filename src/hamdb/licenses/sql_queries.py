#!/usr/bin/env python3

from ..common.settings import DB_SCHEMA_LICENSES

cmd_init = f"""
DROP SCHEMA IF EXISTS {DB_SCHEMA_LICENSES} CASCADE;
CREATE SCHEMA {DB_SCHEMA_LICENSES};

CREATE TABLE IF NOT EXISTS {DB_SCHEMA_LICENSES}.licenses (
    callsign        VARCHAR(10)  NOT NULL,
    authority       VARCHAR(5)   NOT NULL,
    status          CHAR(1)      NULL,
    entity_type     CHAR(1)      NULL,
    grant_date      DATE         NULL,
    expiration_date DATE         NULL,
    name_full       VARCHAR(200) NULL,
    name_first      VARCHAR(100) NULL,
    name_middle     VARCHAR(100) NULL,
    name_last       VARCHAR(100) NULL,
    address_line1   VARCHAR(100) NULL,
    address_line2   VARCHAR(100) NULL,
    address_city    VARCHAR(50)  NULL,
    address_state   VARCHAR(2)   NULL,
    address_zip     VARCHAR(10)  NULL,
    extra_data      JSONB        NULL,

    PRIMARY KEY (callsign)
);

CREATE TABLE IF NOT EXISTS {DB_SCHEMA_LICENSES}.administrators (
    callsign       VARCHAR(10) NOT NULL,
    admin_callsign VARCHAR(10) NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS IX__{DB_SCHEMA_LICENSES}__administrators
    ON {DB_SCHEMA_LICENSES}.administrators (callsign, admin_callsign);

CREATE TABLE IF NOT EXISTS {DB_SCHEMA_LICENSES}.qualifications (
    callsign      VARCHAR(10) NOT NULL,
    qualification CHAR(1)     NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS IX__{DB_SCHEMA_LICENSES}__qualifications
    ON {DB_SCHEMA_LICENSES}.qualifications (callsign, qualification);
"""
