#!/usr/bin/env python3

from ...common.settings import DB_SCHEMA_NXDN, DB_SCHEMA_LICENSES

cmd_full_init = f"""
DROP SCHEMA IF EXISTS {DB_SCHEMA_NXDN} CASCADE;
CREATE SCHEMA {DB_SCHEMA_NXDN};

CREATE TABLE {DB_SCHEMA_NXDN}.nxdnids (
    callsign   VARCHAR(10)  NOT NULL,
    nxdnid     NUMERIC(10)  NULL,
    first_name VARCHAR(100) NULL,
    last_name  VARCHAR(100) NULL,
    city       VARCHAR(100) NULL,
    state      VARCHAR(100) NULL,
    country    VARCHAR(100) NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS IX__{DB_SCHEMA_NXDN}__nxdnids
    ON {DB_SCHEMA_NXDN}.nxdnids (callsign, nxdnid);
"""

cmd_license_insert = f"""
WITH nxdnids AS (
SELECT
    n.callsign,
    jsonb_agg(n.nxdnid) AS nxdn_ids
FROM {DB_SCHEMA_NXDN}.nxdnids n
GROUP BY n.callsign
)
UPDATE {DB_SCHEMA_LICENSES}.licenses ll
    SET extra_data = jsonb_set(COALESCE(ll.extra_data, '{{}}'), '{{nxdn_ids}}', n.nxdn_ids)
FROM nxdnids n
WHERE   ll.callsign = n.callsign;
"""
