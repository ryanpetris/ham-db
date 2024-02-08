#!/usr/bin/env python3

from ...common.settings import DB_SCHEMA_DMR, DB_SCHEMA_LICENSES

cmd_full_init = f"""
DROP SCHEMA IF EXISTS {DB_SCHEMA_DMR} CASCADE;
CREATE SCHEMA {DB_SCHEMA_DMR};

CREATE TABLE {DB_SCHEMA_DMR}.dmrids (
    callsign VARCHAR(10) NOT NULL,
    dmrid    NUMERIC(10) NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS IX__{DB_SCHEMA_DMR}__dmrids
    ON {DB_SCHEMA_DMR}.dmrids (callsign, dmrid);
"""

cmd_license_insert = f"""
WITH dmrids AS (
SELECT
    d.callsign,
    jsonb_agg(d.dmrid) AS dmr_ids
FROM {DB_SCHEMA_DMR}.dmrids d
GROUP BY d.callsign
)
UPDATE {DB_SCHEMA_LICENSES}.licenses ll
    SET extra_data = jsonb_set(COALESCE(ll.extra_data, '{{}}'), '{{dmr_ids}}', d.dmr_ids)
FROM dmrids d
WHERE   ll.callsign = d.callsign;
"""
