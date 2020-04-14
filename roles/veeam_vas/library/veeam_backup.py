#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Markus Kraus <markus.kraus@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: veeam_backup
version_added: '0.1'
short_description: Manages Veeam Servers
description:
   - With the module you can manage Veeam VBR Backup Jobs.
   - Add VMware Backup Jobs
requirements:
   - Windows Server 2019
   - Veeam Backup & Replication 9.5 Update 4b
notes:
  - In order to understand all the returned properties and values please visit the following site
    U(https://helpcenter.veeam.com/docs/backup/powershell/getting_started.html?ver=95u4)
author:
  - Markus Kraus (@vMarkus_K)
options:
  state:
    description:
    - Set to C(present) to add a new backup.
    - Set to C(absent) to remove a backup by id.
    type: str
    choices: [ absent, present ]
    default: present
  type:
    description:
    - Set to C(vi) to add or remove a VMware Backup Job.
    type: str
    choices: [ vi ]
    default: vi
  entiity:
    description:
    - Set to C(tag) to add or remove a Tag as Backup Object.
    type: str
    choices: [ tag ]
    default: tag
  tag:
    description:
    - vSphere Tag Category and Tag Name
    - Example: "Protection\\\\Default"
    type: str
  name:
    description:
    - Name of the Backup Job.
    type: str
  repository:
    description:
    - Backup Repository Name
    type: str
'''

EXAMPLES = r'''
-
'''

RETURN = r'''
-
'''
