#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Chris Arceneaux <carcenea@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: veeam_vbr_upgrade_job_prep
short_description: Backup Job actions before/after upgrading
description:
   - Stops all running backups jobs
   - Saves all enabled backup job names to a file
   - Disables all backup jobs
   - Enables all backup jobs listed in file
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
    - Set to C(disable) to disable backup jobs
    - Set to C(enable) to enable backup jobs
    type: str
    choices: [ disable, enable ]
  jobs_file:
    description:
    - Used as a backup of all jobs enabled before disabling them
    - Full path of file to be used (must use end with .csv)
    type: str
'''

EXAMPLES = r'''
- name: Defining Backup Job file for exporting disabled jobs
  ansible.builtin.set_fact:
    jobs_file: "C:\\install\\DisabledJobs{{ ansible_date_time.iso8601_basic_short }}.csv"
- name: Stopping and disabling all backup jobs
  veeam_vbr_upgrade_job_prep:
    state: disable
    jobs_file: "{{ jobs_file }}"
- name: Enabling all backup jobs in specified file
  veeam_vbr_upgrade_job_prep:
    state: enable
    jobs_file: "{{ jobs_file }}"
'''

RETURN = r'''
-
'''
