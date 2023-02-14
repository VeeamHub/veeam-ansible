#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Chris Arceneaux <carcenea@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: veeam_vbr_cloud_connect_maintenance
short_description: Manages VBR Cloud Connect maintenance mode
description:
   - Enables/Disables Veeam Cloud Connect maintenance mode
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
    - Set to C(enable) to enable Cloud Connect maintenance mode
    - Set to C(disable) to disable Cloud Connect maintenance mode
    type: str
    choices: [ enable, disable ]
'''

EXAMPLES = r'''
- name: Enable Cloud Connect Maintenance Mode
  veeam_vbr_cloud_connect_maintenance:
    state: enable


- name: Disable Cloud Connect Maintenance Mode
  veeam_vbr_cloud_connect_maintenance:
    state: disable
'''

RETURN = r'''
-
'''
