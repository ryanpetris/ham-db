#!/usr/bin/env python3

from ...common.settings import DB_SCHEMA_ISED

cmd_full_init = f"""
DROP SCHEMA IF EXISTS {DB_SCHEMA_ISED} CASCADE;
CREATE SCHEMA {DB_SCHEMA_ISED};

CREATE TABLE {DB_SCHEMA_ISED}.licenses (
    callsign         VARCHAR(6)   NOT NULL,
    first_name       VARCHAR(100) NULL,
    surname          VARCHAR(100) NULL,
    address_line     VARCHAR(100) NULL,
    city             VARCHAR(50)  NULL,
    prov_cd          VARCHAR(2)  NULL,
    postal_code      VARCHAR(10)  NULL,
    qual_a           VARCHAR(1)   NULL,
    qual_b           VARCHAR(1)   NULL,
    qual_c           VARCHAR(1)   NULL,
    qual_d           VARCHAR(1)   NULL,
    qual_e           VARCHAR(1)   NULL,
    club_name        VARCHAR(100) NULL,
    club_name_2      VARCHAR(100) NULL,
    club_address     VARCHAR(100) NULL,
    club_city        VARCHAR(50)  NULL,
    club_prov_cd     VARCHAR(2)  NULL,
    club_postal_code VARCHAR(10)  NULL,

    PRIMARY KEY (callsign)
);
"""
