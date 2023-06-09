#!/usr/bin/python

# Copyright: (c) 2022, Markus Kraus <markus.kraus@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url

ANSIBLE_METADATA = {'metadata_version': '1.11',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: veeam_vbr_rest_servercertificate_info

short_description: Get Current Veeam Backup Server Certificate from RestAPI.

version_added: "1.0.0"

description: Get Current Veeam Backup Server Certificate from RestAPI.

options:
    validate_certs:
        description: Validate SSL certs
        required: false
        default: false
        type: bool
    server_name:
        description: VBR Server Name or IP
        required: true
        type: str
    server_port:
        description: VBR RestAPI Sever Port
        required: false
        default: 9419
        type: str

author:
    - Markus Kraus (@vMarkusK)
'''

EXAMPLES = r'''
- name: Veeam RestAPI Collection
  hosts: localhost
  tasks:
    - name: Test veeam_vbr_rest_servercertificate_info
      veeamhub.veeam.veeam_vbr_rest_servercertificate_info:
        server_name: "<FQDN/IP>"
      register: testout
    - name: Debug Result
      ansible.builtin.debug:
        var: testout
'''

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        server_name=dict(type='str', required=True),
        server_port=dict(type='str', default='9419'),
        validate_certs=dict(type='bool', default='False')
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # General
    apiversion = '1.1-rev0'

    # Payload
    request_server = module.params['server_name']
    request_port = module.params['server_port']
    headers = {
        'accept': 'application/json',
        'x-api-version': apiversion
    }

    request_url = 'https://' + request_server + ':' + request_port + '/api/v1/serverCertificate'

    method = "Get"
    req, info = fetch_url(module, request_url, headers=headers, method=method)

    if info['status'] != 200:
        module.fail_json(msg="Fail: %s" % ("Status: " + str(info['status']) + ", Message: " + str(info['msg'])))

    try:
        result['servercertificate'] = json.loads(req.read())
    except AttributeError:
        module.fail_json(msg='Parsing Response Failed', **result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
