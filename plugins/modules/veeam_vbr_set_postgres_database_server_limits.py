#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2023, Chris Arceneaux <carcenea@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: veeam_vbr_set_postgres_database_server_limits
short_description: Modifies settings of the PostgreSQL instance
description:
   - Apply VBR performance tuning to PostgreSQL server 
   - Supports PostgreSQL running on both Linux & Windows
   - Supports local and remote instances
   - Supports PostgreSQL servers not currently serving as a DB for VBR
requirements:
   - Veeam Backup & Replication 12
notes:
  - In order to understand all the returned properties and values please visit the following site
    U(https://helpcenter.veeam.com/docs/backup/powershell/getting_started.html)
author:
  - Chris Arceneaux (@chris_arceneaux)
options:
  os_type:
    description:
    - Only required if PostgreSQL is on a remote server
    - Specifies the OS of the machine where the PostgreSQL instance is installed
    - Set to C(Windows) if PosgreSQL is installed on Windows
    - Set to C(Linux) if PosgreSQL is installed on Linux
    type: str
    choices: [ Windows, Linux ]
  cpu_count:
    description:
    - Specifies a number of CPU cores that you want to assign to a machine  where the PostgreSQL instance is installed
    type: int
  ram_gb:
    description:
    - Specifies amount of memory in GB that you want to assign to a machine  where the PostgreSQL instance is installed
    type: int
  dump_to_file:
    description:
    - Only required if PostgreSQL is on a remote server and VBR is not currently using it as a DB for VBR
    - Generates a SQL query in a file. The query settings can then be applied to the machine where the PostgreSQL instance is installed
    type: str
'''

EXAMPLES = r'''
- name: Applying tuning on a local PostgreSQL server running as the VBR DB
  veeam_vbr_set_postgres_database_server_limits:

- name: Applying tuning on a remote PostgreSQL server running as the VBR DB
  veeam_vbr_set_postgres_database_server_limits:
    os_type: Windows
    cpu_count: 16
    ram_gb: 64

- name: Applying tuning on a PostgreSQL server not currently serving as a VBR DB
  veeam_vbr_set_postgres_database_server_limits:
    os_type: Windows
    cpu_count: 16
    ram_gb: 64
    dump_to_file: c:\\settings.sql
'''

RETURN = r'''
-
'''
