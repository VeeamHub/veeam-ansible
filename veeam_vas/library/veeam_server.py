#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Markus Kraus <markus.kraus@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: veeam_server
version_added: '0.3'
short_description: Manages Veeam Servers
description:
   - With the module you can manage Veeam VBR Server.
   - Add VMware ESXi Servers
   - Add VMware vCenter Servers
   - Remove VMware ESXi Servers #TBD
   - Remove VMware vCenter Servers #TBD
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
    - Set to C(present) to add a new server.
    - Set to C(absent) to remove a server by id.
    type: str
    choices: [ absent, present ]
    default: present
  type:
    description:
    - Set to C(esxi) to add or remove a VMware ESXi Server.
    - Set to C(vcenter) to add or remove a VMware vCenter Server.
    - Set to C(windows) to add or remove a Windows Server.
    type: str
    choices: [ esxi, vcenter, windows ]
    default: esxi
  credential_id:
    description:
    - Id of the Crendetials for the new Server.
    - use veeam_credential module to create a new one.
    type: str
  name:
    description:
    - IP or FQDN of the new Server.
    type: str
'''

EXAMPLES = r'''
- name: Add root credential
  veeam_credential:
      state: present
      type: standard
      username: root
      password: "{{ root_password }}"
      description: "Lab User for Standalone Host"
  register: root_cred
- name: Add esxi server
  veeam_server:
      state: present
      type: esxi
      credential_id: "{{ root_cred.id }}"
      name: 192.168.234.101
  register: esxi_server
'''

RETURN = r'''
-
'''
