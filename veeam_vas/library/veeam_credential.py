#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Markus Kraus <markus.kraus@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: veeam_credential
version_added: '0.2'
short_description: Manages Veeam Credentials
description:
   - With the module you can manage Veeam VBR Credentials.
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
    - Set to C(present) to create new credentials.
    - Set to C(absent) to remove credentials by id.
    type: str
    choices: [ absent, present ]
    default: present
  type:
    description:
    - Set to C(windows) to create new windows credentials.
    - Set to C(linux) to create new liniux credentials.
    - Set to C(standard) to create new standard credentials.
    type: str
    choices: [ windows, linux, standard ]
    default: standard
  username:
    description:
    -  The username
    type: str
  password:
    description:
    -  The password
    type: str
  id:
    description:
    -  The credential id
    type: str
'''

EXAMPLES = r'''
  - name: Add credential
    veeam_credential:
        state: present
        type: windows
        username: Administrator
        password: ChangeMe
        description: dummy description
    register: my_cred
  - name: Debug Veeam Credentials
    debug:
        var: my_cred
  - name: Remove credential
    veeam_credential:
        state: absent
        id: "{{ my_cred.id }}"
'''

RETURN = r'''
id:
  description: the id of the newly created credential
  returned: present
  type: str
  sample: "57d818b1-21fd-4ee9-ae37-2cfcd0757629"
'''
