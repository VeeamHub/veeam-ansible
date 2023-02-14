#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Chris Arceneaux <carcenea@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.11',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: pending_reboot_check
short_description: Checks if there is a pending reboot
description:
   - Retrieves registry keys related to pending reboots
   - Checks them to see if there exists a pending reboot
   - Returns boolean to denote pending reboot status
   - If true, pending reboot flag has been detected
requirements:
   - Windows Server 2019
   - Windows Server 2022
notes:
  - Base code taken from U(https://github.com/bcwilhite/PendingReboot/)
  - Values are pulled from the registry
author:
  - Chris Arceneaux (@chris_arceneaux)
'''

EXAMPLES = r'''
- name: Checking to see if there is a pending reboot
  pending_reboot_check:
  register: check
- name: Rebooting if necessary
  ansible.windows.win_reboot:
  when: check.pending_reboot|bool
'''

RETURN = r'''
-
'''
