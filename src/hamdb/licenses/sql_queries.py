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

cmd_license_query = f"""
SELECT
    l.callsign,
    'L' AS type,
    to_jsonb(l.*) AS data
FROM {DB_SCHEMA_LICENSES}.licenses l
WHERE   l.callsign = ANY(%(callsigns)s)
UNION ALL
SELECT
    q.callsign,
    'Q' AS type,
    to_jsonb(q.*) - 'callsign' AS data
FROM {DB_SCHEMA_LICENSES}.qualifications q
WHERE   q.callsign = ANY(%(callsigns)s)
UNION ALL
SELECT
    a.callsign,
    'A' AS type,
    to_jsonb(a.*) - 'callsign' AS data
FROM {DB_SCHEMA_LICENSES}.administrators a
WHERE   a.callsign = ANY(%(callsigns)s);
"""

cmd_stats_query = f"""
WITH active_licenses AS (
    SELECT
        'active_licenses' AS type,
        l.authority,
        COUNT(*) AS count
    FROM {DB_SCHEMA_LICENSES}.licenses l
    WHERE l.status != 'N'
    GROUP BY l.authority
), active_licenses_by_qualification AS (
    SELECT
        'active_licenses_by_qualification' AS type,
        l.authority,
        q.qualification,
        COUNT(*) AS count
    FROM {DB_SCHEMA_LICENSES}.licenses l
    INNER JOIN {DB_SCHEMA_LICENSES}.qualifications q ON l.callsign = q.callsign
    WHERE l.status != 'N'
    GROUP BY l.authority, q.qualification
), active_licenses_by_state AS (
    SELECT
        'active_licenses_by_state' AS type,
        l.authority,
        UPPER(l.address_state) AS state,
        COUNT(*) AS count
    FROM {DB_SCHEMA_LICENSES}.licenses l
    WHERE l.status != 'N'
    GROUP BY l.authority, UPPER(l.address_state)
), active_dmr_ids AS (
    SELECT
        'active_dmr_ids' AS type,
        l.authority,
        SUM(jsonb_array_length(l.extra_data -> 'dmr_ids')) AS count
    FROM {DB_SCHEMA_LICENSES}.licenses l
    WHERE   l.status != 'N'
        AND l.extra_data -> 'dmr_ids' IS NOT NULL
    GROUP BY l.authority
), active_nxdn_ids AS (
    SELECT
        'active_nxdn_ids' AS type,
        l.authority,
        SUM(jsonb_array_length(l.extra_data -> 'nxdn_ids')) AS count
    FROM {DB_SCHEMA_LICENSES}.licenses l
    WHERE   l.status != 'N'
        AND l.extra_data -> 'nxdn_ids' IS NOT NULL
    GROUP BY l.authority
), results AS (
    SELECT to_jsonb(q) AS result FROM active_licenses q
    UNION ALL
    SELECT to_jsonb(q) AS result FROM active_licenses_by_qualification q
    UNION ALL
    SELECT to_jsonb(q) AS result FROM active_licenses_by_state q
    UNION ALL
    SELECT to_jsonb(q) AS result FROM active_dmr_ids q
    UNION ALL
    SELECT to_jsonb(q) AS result FROM active_nxdn_ids q
)
INSERT INTO statistics (data)
SELECT jsonb_agg(q.result) AS data FROM results q;
"""
