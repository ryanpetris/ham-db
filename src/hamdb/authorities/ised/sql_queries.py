#!/usr/bin/env python3

from ...common.settings import DB_SCHEMA_ISED, DB_SCHEMA_LICENSES

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

cmd_license_insert = f"""
INSERT INTO {DB_SCHEMA_LICENSES}.licenses
    (callsign, authority, status, entity_type, grant_date, expiration_date,
     name_full, name_first, name_middle, name_last,
     address_line1, address_line2, address_city, address_state, address_zip,
     extra_data)
SELECT
    l.callsign,
    'ISED' AS authority,
    'A' AS status,
    'I' AS entity_type,
    CAST(NULL AS DATE) AS grant_date,
    CAST(NULL AS DATE) AS expiration_date,
    CONCAT(l.surname, ', ', l.first_name) AS name_full,
    l.first_name AS name_first,
    NULL AS name_middle,
    l.surname AS name_last,
    l.address_line AS address_line1,
    NULL AS address_line2,
    l.city AS address_city,
    l.prov_cd AS address_state,
    l.postal_code AS address_zip,
    CAST(NULL AS JSONB) AS extra_data
FROM {DB_SCHEMA_ISED}.licenses l
WHERE   l.club_name IS NULL
UNION ALL
SELECT
    l.callsign,
    'ISED' AS authority,
    'A' AS status,
    'C' AS entity_type,
    CAST(NULL AS DATE) AS grant_date,
    CAST(NULL AS DATE) AS expiration_date,
    l.club_name AS name_full,
    NULL AS name_first,
    NULL AS name_middle,
    NULL AS name_last,
    CASE
        WHEN l.club_name_2 IS NOT NULL THEN l.club_name_2
        ELSE l.club_address
    END AS address_line1,
    CASE
        WHEN l.club_name_2 IS NOT NULL THEN l.club_address
        ELSE NULL
    END AS address_line2,
    l.club_city AS address_city,
    l.club_prov_cd AS address_state,
    l.club_postal_code AS address_zip,
    CAST(NULL AS JSONB) AS extra_data
FROM {DB_SCHEMA_ISED}.licenses l
WHERE   l.club_name IS NOT NULL
ON CONFLICT (callsign) DO UPDATE
    SET authority = EXCLUDED.authority,
        status = EXCLUDED.status,
        entity_type = EXCLUDED.entity_type,
        grant_date = EXCLUDED.grant_date,
        expiration_date = EXCLUDED.expiration_date,
        name_first = EXCLUDED.name_first,
        name_middle = EXCLUDED.name_middle,
        name_last = EXCLUDED.name_last,
        address_line1 = EXCLUDED.address_line1,
        address_city = EXCLUDED.address_city,
        address_state = EXCLUDED.address_state,
        address_zip = EXCLUDED.address_zip,
        extra_data = EXCLUDED.extra_data;

INSERT INTO {DB_SCHEMA_LICENSES}.administrators
    (callsign, admin_callsign)
SELECT
    l.callsign,
    MIN(ll.callsign) AS admin_callsign
FROM {DB_SCHEMA_ISED}.licenses l
INNER JOIN {DB_SCHEMA_ISED}.licenses ll ON ll.club_name IS NULL AND l.first_name = ll.first_name AND l.surname = ll.surname AND l.postal_code = ll.postal_code
WHERE   l.club_name IS NOT NULL
GROUP BY l.callsign
ON CONFLICT (callsign, admin_callsign) DO NOTHING;

UPDATE {DB_SCHEMA_LICENSES}.licenses ll
    SET extra_data = jsonb_set(COALESCE(ll.extra_data, '{{}}'), '{{_administrators}}', jsonb_build_array(jsonb_build_object(
            'authority', 'ISED',
            'entity_type', 'I',
            'name_full', CONCAT(l.surname, ', ', l.first_name),
            'name_first', l.first_name,
            'name_last', l.surname,
            'address_line1', l.address_line,
            'address_city', l.city,
            'address_state', l.prov_cd,
            'address_zip', l.postal_code
        )))
FROM {DB_SCHEMA_ISED}.licenses l
WHERE   l.callsign = ll.callsign
    AND ll.entity_type = 'C'
    AND NOT EXISTS (
            SELECT *
            FROM {DB_SCHEMA_LICENSES}.administrators a
            WHERE   a.callsign = ll.callsign
        );

INSERT INTO {DB_SCHEMA_LICENSES}.qualifications
    (callsign, qualification)
SELECT
    l.callsign,
    q.qualification
FROM {DB_SCHEMA_ISED}.licenses l
CROSS JOIN unnest(array[l.qual_a, l.qual_b, l.qual_c, l.qual_d, l.qual_e]) AS q(qualification)
WHERE	q.qualification IS NOT NULL
ON CONFLICT (callsign, qualification) DO NOTHING;
"""
