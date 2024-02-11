#!/usr/bin/env python3

cmd_init = f"""
CREATE TABLE IF NOT EXISTS settings (
    name  VARCHAR(255) NOT NULL,
    value VARCHAR(255) NOT NULL,

    PRIMARY KEY (name)
);

CREATE TABLE IF NOT EXISTS statistics (
    id   SERIAL    PRIMARY KEY,
    date TIMESTAMP NOT NULL    DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
    data JSONB     NOT NULL
);
"""
