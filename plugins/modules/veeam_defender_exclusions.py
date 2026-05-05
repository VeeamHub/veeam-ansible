#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Chris Arceneaux <carcenea@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: veeam_defender_exclusions
short_description: Manage Windows Defender exclusions
description:
   - Adds or removes Windows Defender exclusions for paths, processes, or extensions
   - Supports idempotent management of exclusion lists
requirements:
   - Windows Defender
   - Windows Server 2019
   - Windows Server 2022
   - Windows Server 2025
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
    required: true
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
- name: Adding path exclusions to Windows Defender
  veeam_defender_exclusions:
    state: present
    exclusion_type: path
    exclusions:
      - "C:\\Program Files\\Veeam"
      - "C:\\VeeamBackup"

- name: Adding process exclusions to Windows Defender
  veeam_defender_exclusions:
    state: present
    exclusion_type: process
    exclusions:
      - "veeam.backup.agent.configurationtool.exe"

- name: Removing extension exclusions from Windows Defender
  veeam_defender_exclusions:
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
msg:
  description: Status message describing the result of the operation.
  returned: always
  type: str
  sample: "Exclusions have been updated."
exclusions:
  description: List of currently configured exclusions of the specified type after the operation.
  returned: always
  type: list
  elements: str
  sample: ["C:\\Program Files\\Veeam", "C:\\VeeamBackup"]
'''

import json
import os
import subprocess

from ansible.module_utils.basic import AnsibleModule


def run_module():
    module_args = dict(
        state=dict(type='str', required=True, choices=['present', 'absent']),
        exclusion_type=dict(type='str', required=True, choices=['path', 'process', 'extension']),
        exclusions=dict(type='list', elements='str', required=True),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    state = module.params['state']
    exclusion_type = module.params['exclusion_type']
    exclusions = module.params['exclusions']
    exclusions_str = ';'.join(exclusions)

    ps1_path = os.path.join(os.path.dirname(__file__), 'veeam_defender_exclusions.ps1')

    result = subprocess.run(
        ['powershell.exe', '-NonInteractive', '-NoProfile', '-ExecutionPolicy', 'Bypass',
         '-File', ps1_path,
         '-state', state,
         '-exclusion_type', exclusion_type,
         '-exclusions', exclusions_str],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if result.returncode != 0:
        module.fail_json(
            msg='PowerShell script failed: ' + result.stderr.decode('utf-8', errors='replace').strip()
        )

    try:
        output = json.loads(result.stdout.decode('utf-8', errors='replace').strip())
    except ValueError as e:
        module.fail_json(
            msg='Failed to parse PowerShell output as JSON: ' + str(e),
            stdout=result.stdout.decode('utf-8', errors='replace')
        )

    module.exit_json(
        changed=output.get('changed', False),
        msg=output.get('msg', ''),
        exclusions=output.get('exclusions', [])
    )


def main():
    run_module()


if __name__ == '__main__':
    main()
