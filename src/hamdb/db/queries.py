#!/usr/bin/env python3

cmd_init = f"""
CREATE TABLE IF NOT EXISTS settings (
    name  VARCHAR(255) NOT NULL,
    value VARCHAR(255) NOT NULL,

    PRIMARY KEY (name)
);
"""
