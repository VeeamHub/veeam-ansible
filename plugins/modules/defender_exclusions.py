#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Chris Arceneaux <carcenea@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: defender_exclusions
short_description: Manage Windows Defender exclusions
description:
   - Adds or removes Windows Defender exclusions for paths, processes, or extensions
   - Supports idempotent management of exclusion lists
   - Can be used as an alternative to configuring exclusions via Active Directory Group Policy
requirements:
   - Windows Defender
   - Windows Server 2019
   - Windows Server 2022
   - Windows Server 2025
version_added: "2.3.8"
notes:
  - In order to understand all the returned properties and values please visit the following site
    U(https://docs.microsoft.com/en-us/powershell/module/defender/add-mppreference)
author:
  - Chris Arceneaux (@chris_arceneaux)
options:
  state:
    description:
    - Set to C(present) to add exclusions
    - Set to C(absent) to remove exclusions
    type: str
    choices: [ present, absent ]
    default: present
  exclusion_type:
    description:
    - Type of Windows Defender exclusion to manage
    - C(path) manages path-based exclusions
    - C(process) manages process-based exclusions
    - C(extension) manages extension-based exclusions
    type: str
    choices: [ path, process, extension ]
    required: true
  exclusions:
    description:
    - List of paths, processes, or extensions to add or remove
    type: list
    elements: str
    required: true
'''

EXAMPLES = r'''
# Reference (VBR): https://www.veeam.com/kb1999
- name: Setting Windows Defender Exclusions for Veeam Backup & Replication
  veeamhub.veeam.defender_exclusions:
    state: present
    exclusion_type: path
    exclusions:
      - C:\Program Files\Veeam\Backup and Replication\Threat Hunter
      - C:\Program Files\Veeam
      - C:\Program Files (x86)\Veeam
      - C:\Program Files\Common Files\Veeam
      - C:\Program Files (x86)\Common Files\Veeam
      - C:\Program Files\PostgreSQL
      - C:\VeeamFLR
      - C:\Windows\Veeam
      - C:\ProgramData\Veeam
      - C:\Windows\Temp\*\veeamflr-*.flat
      - C:\Windows\SystemTemp\veeam-*.json
      - C:\Windows\Temp\VeeamBackup
      - C:\Windows\Temp\VeeamBackupTemp
      - C:\Windows\Temp\veeamdumprecorder
      - C:\Windows\TEMP\VeeamForeignSessionContext*
      - C:\VBRCatalog

- name: Setting Windows Defender Exclusions for Veeam Backup Enterprise Manager
  veeamhub.veeam.defender_exclusions:
    state: present
    exclusion_type: path
    exclusions:
      - C:\Program Files\Veeam
      - C:\Program Files (x86)\Veeam
      - C:\Program Files\Common Files\Veeam
      - C:\Program Files (x86)\Common Files\Veeam
      - C:\VeeamFLR
      - C:\Windows\Veeam
      - C:\ProgramData\Veeam
      - C:\Windows\Temp\*\veeamflr-*.flat
      - C:\Windows\SystemTemp\veeam-*.json
      - C:\Windows\Temp\VeeamBackup
      - C:\Windows\Temp\VeeamBackupTemp
      - C:\Windows\Temp\veeamdumprecorder

- name: Setting Windows Defender Exclusions for Veeam Backup & Replication Console
  veeamhub.veeam.defender_exclusions:
    state: present
    exclusion_type: path
    exclusions:
      - C:\Program Files\Veeam
      - C:\Program Files (x86)\Veeam
      - C:\Program Files\Common Files\Veeam
      - C:\Program Files (x86)\Common Files\Veeam
      - C:\VeeamFLR
      - C:\Windows\Veeam
      - C:\ProgramData\Veeam
      - C:\Windows\Temp\*\veeamflr-*.flat
      - C:\Windows\SystemTemp\veeam-*.json
      - C:\Windows\Temp\VeeamBackup
      - C:\Windows\Temp\VeeamBackupTemp
      - C:\Windows\Temp\veeamdumprecorder

# Reference (VSPC): https://www.veeam.com/kb2644
- name: Setting Windows Defender Exclusions for Veeam Service Provider Console Server
  veeamhub.veeam.defender_exclusions:
    state: present
    exclusion_type: path
    exclusions:
      - C:\Program Files\Veeam
      - C:\Program Files\Common Files\Veeam
      - C:\Program Files (x86)\Common Files\Veeam
      - C:\ProgramData\Veeam
      - C:\Windows\Veeam

- name: Adding path exclusions to Windows Defender
  veeamhub.veeam.defender_exclusions:
    state: present
    exclusion_type: path
    exclusions:
      - "C:\Program Files\Veeam"
      - "C:\VeeamBackup"

- name: Adding process exclusions to Windows Defender
  veeamhub.veeam.defender_exclusions:
    state: present
    exclusion_type: process
    exclusions:
      - "veeam.backup.agent.configurationtool.exe"

- name: Removing extension exclusions from Windows Defender
  veeamhub.veeam.defender_exclusions:
    state: absent
    exclusion_type: extension
    exclusions:
      - ".vbk"
      - ".vib"
'''

RETURN = r'''
changed:
  description: Whether any exclusions were added or removed.
  returned: always
  type: bool
  sample: true
changes:
  description: List of changes made during the run, one entry per exclusion added or removed.
  returned: when changes were made
  type: list
  elements: str
  sample:
    - "Added path exclusion: C:\Program Files\Veeam"
    - "Removed extension exclusion: .vbk"
'''
