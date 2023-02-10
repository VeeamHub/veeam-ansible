#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Chris Arceneaux <carcenea@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: veeam_vbr_config_backup
short_description: Manages VBR configuration backup job
description:
   - Set VBR configuration backup job settings #TBD
   - Start adhoc VBR configuration backup job
requirements:
   - Veeam Backup & Replication 9.5 Update 3
notes:
  - In order to understand all the returned properties and values please visit the following site
    U(https://helpcenter.veeam.com/docs/backup/powershell/getting_started.html)
author:
  - Chris Arceneaux (@chris_arceneaux)
options:
  state:
    description:
    - Set to C(present) to enable the VBR configuration backup job
    - Set to C(absent) to disable the VBR configuration backup job
    - Set to C(adhoc) to start a one-time VBR configuration backup job
    type: str
    choices: [ present, absent, adhoc ]
    default: present
'''

EXAMPLES = r'''
- name: Start adhoc VBR configuration backup job
  veeam_vbr_config_backup:
    state: adhoc
'''

RETURN = r'''
-
'''
