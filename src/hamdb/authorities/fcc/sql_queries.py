#!/usr/bin/env python3

from ...common.settings import DB_SCHEMA_FCC, DB_SCHEMA_LICENSES

cmd_full_init = f"""
DROP SCHEMA IF EXISTS {DB_SCHEMA_FCC} CASCADE;
CREATE SCHEMA {DB_SCHEMA_FCC};

CREATE TABLE {DB_SCHEMA_FCC}.am (
    record_type                CHAR(2)       NOT NULL,
    unique_system_identifier   NUMERIC(9, 0) NOT NULL,
    uls_file_num               VARCHAR(14)   NULL,
    ebf_number                 VARCHAR(30)   NULL,
    callsign                   VARCHAR(10)   NULL,
    operator_class             VARCHAR(1)    NULL,
    group_code                 VARCHAR(1)    NULL,
    region_code                SMALLINT      NULL,
    trustee_callsign           VARCHAR(10)   NULL,
    trustee_indicator          VARCHAR(1)    NULL,
    physician_certification    VARCHAR(1)    NULL,
    ve_signature               VARCHAR(1)    NULL,
    systematic_callsign_change VARCHAR(1)    NULL,
    vanity_callsign_change     VARCHAR(1)    NULL,
    vanity_relationship        VARCHAR(12)   NULL,
    previous_callsign          VARCHAR(10)   NULL,
    previous_operator_class    VARCHAR(1)    NULL,
    trustee_name               VARCHAR(50)   NULL,

    PRIMARY KEY (unique_system_identifier)
);

CREATE INDEX IF NOT EXISTS IX__{DB_SCHEMA_FCC}__am__callsign
    ON {DB_SCHEMA_FCC}.am (callsign);

CREATE INDEX IF NOT EXISTS IX__{DB_SCHEMA_FCC}__am__previous_callsign
    ON {DB_SCHEMA_FCC}.am (previous_callsign)
    INCLUDE (callsign);

CREATE INDEX IF NOT EXISTS IX__{DB_SCHEMA_FCC}__am__trustee_callsign
    ON {DB_SCHEMA_FCC}.am (trustee_callsign)
    INCLUDE (callsign);

CREATE TABLE {DB_SCHEMA_FCC}.co (
    record_type              CHAR(2)       NOT NULL,
    unique_system_identifier NUMERIC(9, 0) NOT NULL,
    uls_file_num             VARCHAR(14)   NULL,
    callsign                 VARCHAR(10)   NULL,
    comment_date             VARCHAR(10)   NULL,
    description              VARCHAR(255)  NULL,
    status_code              VARCHAR(1)    NULL,
    status_date              TIMESTAMP     NULL
);

CREATE INDEX IF NOT EXISTS IX__{DB_SCHEMA_FCC}__co__callsign
    ON {DB_SCHEMA_FCC}.co (callsign);

CREATE TABLE {DB_SCHEMA_FCC}.en (
    record_type              CHAR(2)       NOT NULL,
    unique_system_identifier NUMERIC(9, 0) NOT NULL,
    uls_file_num             VARCHAR(14)   NULL,
    ebf_number               VARCHAR(30)   NULL,
    callsign                 VARCHAR(10)   NULL,
    entity_type              VARCHAR(2)    NULL,
    licensee_id              VARCHAR(9)    NULL,
    entity_name              VARCHAR(200)  NULL,
    first_name               VARCHAR(20)   NULL,
    mi                       VARCHAR(1)    NULL,
    last_name                VARCHAR(20)   NULL,
    suffix                   VARCHAR(3)    NULL,
    phone                    VARCHAR(10)   NULL,
    fax                      VARCHAR(10)   NULL,
    email                    VARCHAR(50)   NULL,
    street_address           VARCHAR(60)   NULL,
    city                     VARCHAR(20)   NULL,
    state                    VARCHAR(2)    NULL,
    zip_code                 VARCHAR(9)    NULL,
    po_box                   VARCHAR(20)   NULL,
    attention_line           VARCHAR(35)   NULL,
    sgin                     VARCHAR(3)    NULL,
    frn                      VARCHAR(10)   NULL,
    applicant_type_code      VARCHAR(1)    NULL,
    applicant_type_other     VARCHAR(40)   NULL,
    status_code              VARCHAR(1)    NULL,
    status_date              TIMESTAMP     NULL,
    lic_category_code        VARCHAR(1)    NULL,
    linked_license_id        NUMERIC(9, 0) NULL,
    linked_callsign          VARCHAR(10)   NULL,

    PRIMARY KEY (unique_system_identifier)
);

CREATE INDEX IF NOT EXISTS IX__{DB_SCHEMA_FCC}__en__callsign
    ON {DB_SCHEMA_FCC}.en (callsign);
    
CREATE INDEX IF NOT EXISTS IX__{DB_SCHEMA_FCC}__en__frn
    ON {DB_SCHEMA_FCC}.en (frn);

CREATE TABLE {DB_SCHEMA_FCC}.hd (
    record_type                  CHAR(2)       NOT NULL,
    unique_system_identifier     NUMERIC(9, 0) NOT NULL,
    uls_file_num                 VARCHAR(14)   NULL,
    ebf_number                   VARCHAR(30)   NULL,
    callsign                     VARCHAR(10)   NULL,
    license_status               VARCHAR(1)    NULL,
    radio_service_code           VARCHAR(2)    NULL,
    grant_date                   VARCHAR(10)   NULL,
    expired_date                 VARCHAR(10)   NULL,
    cancellation_date            VARCHAR(10)   NULL,
    eligibility_rule_num         VARCHAR(10)   NULL,
    applicant_type_code_reserved VARCHAR(1)    NULL,
    alien                        VARCHAR(1)    NULL,
    alien_government             VARCHAR(1)    NULL,
    alien_corporation            VARCHAR(1)    NULL,
    alien_officer                VARCHAR(1)    NULL,
    alien_control                VARCHAR(1)    NULL,
    revoked                      VARCHAR(1)    NULL,
    convicted                    VARCHAR(1)    NULL,
    adjudged                     VARCHAR(1)    NULL,
    involved_reserved            VARCHAR(1)    NULL,
    common_carrier               VARCHAR(1)    NULL,
    non_common_carrier           VARCHAR(1)    NULL,
    private_comm                 VARCHAR(1)    NULL,
    fixed                        VARCHAR(1)    NULL,
    mobile                       VARCHAR(1)    NULL,
    radiolocation                VARCHAR(1)    NULL,
    satellite                    VARCHAR(1)    NULL,
    developmental_or_sta         VARCHAR(1)    NULL,
    interconnected_service       VARCHAR(1)    NULL,
    certifier_first_name         VARCHAR(20)   NULL,
    certifier_mi                 VARCHAR(1)    NULL,
    certifier_last_name          VARCHAR(20)   NULL,
    certifier_suffix             VARCHAR(3)    NULL,
    certifier_title              VARCHAR(40)   NULL,
    gender                       VARCHAR(1)    NULL,
    african_american             VARCHAR(1)    NULL,
    native_american              VARCHAR(1)    NULL,
    hawaiian                     VARCHAR(1)    NULL,
    asian                        VARCHAR(1)    NULL,
    white                        VARCHAR(1)    NULL,
    ethnicity                    VARCHAR(1)    NULL,
    effective_date               VARCHAR(10)   NULL,
    last_action_date             VARCHAR(10)   NULL,
    auction_id                   INT           NULL,
    reg_stat_broad_serv          VARCHAR(1)    NULL,
    band_manager                 VARCHAR(1)    NULL,
    type_serv_broad_serv         VARCHAR(1)    NULL,
    alien_ruling                 VARCHAR(1)    NULL,
    licensee_name_change         VARCHAR(1)    NULL,
    whitespace_ind               VARCHAR(1)    NULL,
    additional_cert_choice       VARCHAR(1)    NULL,
    additional_cert_answer       VARCHAR(1)    NULL,
    discontinuation_ind          VARCHAR(1)    NULL,
    regulatory_compliance_ind    VARCHAR(1)    NULL,
    eligibility_cert_900         VARCHAR(1)    NULL,
    transition_plan_cert_900     VARCHAR(1)    NULL,
    return_spectrum_cert_900     VARCHAR(1)    NULL,
    payment_cert_900             VARCHAR(1)    NULL,
 
    PRIMARY KEY (unique_system_identifier)
);

CREATE INDEX IF NOT EXISTS IX__{DB_SCHEMA_FCC}__hd__callsign
    ON {DB_SCHEMA_FCC}.hd (callsign);

CREATE TABLE {DB_SCHEMA_FCC}.hs (
    record_type              CHAR(2)       NOT NULL,
    unique_system_identifier NUMERIC(9, 0) NOT NULL,
    uls_file_num             VARCHAR(14)   NULL,
    callsign                 VARCHAR(10)   NULL,
    log_date                 VARCHAR(10)   NULL,
    code                     VARCHAR(6)    NULL
);

CREATE INDEX IF NOT EXISTS IX__{DB_SCHEMA_FCC}__hs__callsign
    ON {DB_SCHEMA_FCC}.hs (callsign);

CREATE TABLE {DB_SCHEMA_FCC}.la (
    record_type              CHAR(2)       NOT NULL,
    unique_system_identifier NUMERIC(9, 0) NOT NULL,
    callsign                 VARCHAR(10)   NULL,
    attachment_code          VARCHAR(1)    NULL,
    attachment_desc          VARCHAR(60)   NULL,
    attachment_date          VARCHAR(10)   NULL,
    attachment_filename      VARCHAR(60)   NULL,
    action_performed         VARCHAR(1)    NULL
);

CREATE INDEX IF NOT EXISTS IX__{DB_SCHEMA_FCC}__la__callsign
    ON {DB_SCHEMA_FCC}.la (callsign);

CREATE TABLE {DB_SCHEMA_FCC}.sc (
    record_type              CHAR(2)       NOT NULL,
    unique_system_identifier NUMERIC(9, 0) NOT NULL,
    uls_file_num             VARCHAR(14)   NULL,
    ebf_number               VARCHAR(30)   NULL,
    callsign                 VARCHAR(10)   NULL,
    special_condition_type   VARCHAR(1)    NULL,
    special_condition_code   INT           NULL,
    status_code              VARCHAR(1)    NULL,
    status_date              TIMESTAMP     NULL
);

CREATE INDEX IF NOT EXISTS IX__{DB_SCHEMA_FCC}__sc__callsign
    ON {DB_SCHEMA_FCC}.sc (callsign);

CREATE TABLE {DB_SCHEMA_FCC}.sf (
    record_type              CHAR(2)       NOT NULL,
    unique_system_identifier NUMERIC(9, 0) NOT NULL,
    uls_file_num             VARCHAR(14)   NULL,
    ebf_number               VARCHAR(30)   NULL,
    callsign                 VARCHAR(10)   NULL,
    lic_freeform_cond_type   VARCHAR(1)    NULL,
    unique_lic_freeform_id   NUMERIC(9, 0) NULL,
    sequence_number          INT           NULL,
    lic_freeform_condition   VARCHAR(255)  NULL,
    status_code              VARCHAR(1)    NULL,
    status_date              TIMESTAMP     NULL,

    PRIMARY KEY (unique_system_identifier)
);

CREATE INDEX IF NOT EXISTS IX__{DB_SCHEMA_FCC}__sf__callsign
    ON {DB_SCHEMA_FCC}.sf (callsign);
"""

cmd_license_insert = f"""
INSERT INTO {DB_SCHEMA_LICENSES}.licenses
    (callsign, authority, status, entity_type, grant_date, expiration_date,
     name_full, name_first, name_middle, name_last,
     address_line1, address_line2, address_city, address_state, address_zip,
     extra_data)
SELECT
    en.callsign,
    'FCC' AS authority,
    CASE UPPER(hd.license_status)
        WHEN 'A' THEN 'A'
        WHEN 'C' THEN 'N'
        WHEN 'E' THEN 'N'
        WHEN 'T' THEN 'N'
        WHEN 'L' THEN 'P'
        WHEN 'X' THEN 'P'
        ELSE NULL
    END AS status,
    CASE UPPER(en.applicant_type_code)
        WHEN 'I' THEN 'I'
        WHEN 'B' THEN 'C'
        WHEN 'G' THEN 'G'
        WHEN 'M' THEN 'M'
        WHEN 'R' THEN 'R'
        ELSE NULL
    END AS entity_type,
    TO_DATE(hd.grant_date, 'MM/DD/YYYY') AS grant_date,
    TO_DATE(hd.expired_date, 'MM/DD/YYYY') AS expiration_date,
    en.entity_name AS name_full,
    en.first_name AS name_first,
    en.mi AS name_middle,
    en.last_name AS name_last,
    en.street_address AS address_line1,
    NULL AS address_line2,
    en.city AS address_city,
    en.state AS address_state,
    en.zip_code AS address_zip,
    jsonb_build_object(
        'frn', en.frn,
        'licensee_id', en.licensee_id,
        'unique_system_identifier', en.unique_system_identifier,
        'is_convicted_felon', CASE UPPER(hd.convicted)
            WHEN 'Y' THEN true
            WHEN 'N' THEN false
            ELSE NULL
        END
    ) AS extra_data
FROM {DB_SCHEMA_FCC}.en en
INNER JOIN {DB_SCHEMA_FCC}.hd hd ON hd.unique_system_identifier = en.unique_system_identifier
LEFT OUTER JOIN {DB_SCHEMA_FCC}.am am ON am.unique_system_identifier = en.unique_system_identifier
WHERE   UPPER(hd.license_status) IN ('A', 'L', 'X')
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
    am.callsign,
    am.trustee_callsign AS admin_callsign
FROM {DB_SCHEMA_FCC}.am
INNER JOIN {DB_SCHEMA_LICENSES}.licenses cl ON am.callsign = cl.callsign AND am.unique_system_identifier = (cl.extra_data ->> 'unique_system_identifier')::numeric
INNER JOIN {DB_SCHEMA_LICENSES}.licenses il ON am.trustee_callsign =  il.callsign
ON CONFLICT (callsign, admin_callsign) DO NOTHING;

INSERT INTO {DB_SCHEMA_LICENSES}.qualifications
    (callsign, qualification)
SELECT
    am.callsign,
    UPPER(am.operator_class) AS qualification
FROM {DB_SCHEMA_FCC}.am
INNER JOIN {DB_SCHEMA_LICENSES}.licenses l ON am.callsign = l.callsign AND am.unique_system_identifier = (l.extra_data ->> 'unique_system_identifier')::numeric
WHERE   am.operator_class IS NOT NULL
ON CONFLICT (callsign, qualification) DO NOTHING;
"""
