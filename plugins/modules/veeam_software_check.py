#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Chris Arceneaux <carcenea@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: veeam_software_check
short_description: Checks if software is installed
description:
   - Retrieves a list of all software installed
   - Checks list to see if specified software is present
   - Returns boolean to denote installation status
   - If true, software version is returned as well
requirements:
   - Windows Server 2019
   - Windows Server 2022
notes:
  - Function taken from U(https://helpcenter.veeam.com/docs/backup/powershell/getting_started.html)
  - Values are pulled from the registry
author:
  - Chris Arceneaux (@chris_arceneaux)
options:
  name:
    description:
    - Software name that is checked for installation status
    - Wildcards (*) are supported but may cause multiple responses
    type: str
  allow_multiple:
    description:
    - Boolean to allow multiple responses
    - Default is to fail task if multiple responses received
    type: bool
    default: false
'''

EXAMPLES = r'''
- name: Checking to see if Veeam Backup & Replication Server is installed
  veeam_software_check:
    name: "Veeam Backup & Replication Server"


- name: Checking to see if Veeam software is installed
  veeam_software_check:
    name: "Veeam*"
    allow_multiple: true
  register: software
- ansible.builtin.debug:
    var: software.output | from_json
'''

RETURN = r'''
-
'''
