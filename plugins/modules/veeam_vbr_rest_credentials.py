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
module: veeam_vbr_rest_credentials

short_description: Add and Remove Veeam Backup & Replication Credentials.

version_added: "1.0.0"

description: Add and Remove Veeam Backup & Replication Credentials.

options:
    validate_certs:
        description: Validate SSL certs.
        required: false
        default: false
        type: bool
    state:
        description:
        - Indicate desired state.
        default: present
        type: str
        choices: ['present', 'absent']
    server_name:
        description: VBR Server Name or IP
        required: true
        type: str
    server_port:
        description: VBR RestAPI Sever Port
        required: false
        default: 9419
        type: str
    server_username:
        description: VBR Server Username
        required: true
        type: str
    server_password:
        description: VBR Server password
        required: true
        type: str
    id:
        description: VBR Server credential ID
        required: false
        type: str
    username:
        description: VBR Server credential username
        required: false
        type: str
    password:
        description: VBR Server credential password
        required: false
        type: str
    description:
        description: VBR Server credential description
        required: false
        type: str
    type:
        description:
        - Set to C(Windows) to create new windows credentials.
        - Set to C(Linux) to create new liniux credentials.
        - Set to C(Standard) to create new standard credentials.
        type: str
        choices: [ Windows, Linux, Standard ]
        default: Standard

author:
    - Markus Kraus (@vMarkusK)
'''

EXAMPLES = r'''
- name: Test Veeam RestAPI Collection
  hosts: localhost
  tasks:
    - name: Test veeam_vbr_rest_credentials Create
      veeamhub.veeam.veeam_vbr_rest_credentials:
        server_name: "<FQDN/IP>"
        server_username: "<Username>"
        server_password: "<Password>"
        type: "Linux"
        username: "<Username>"
        password: "<Password>"
        description: "Created by Ansible RestAPI Module"
      register: create_cred
    - name: Debug Result
      ansible.builtin.debug:
        var: create_cred
    - name: Test veeam_vbr_credentials Delete
      veeamhub.veeam.veeam_vbr_rest_credentials:
        server_name: "<FQDN/IP>"
        server_username: "<Username>"
        server_password: "<Password>"
        id: "{{ create_cred.msg.id }}"
        state: absent
      register: delete_cred
    - name: Debug Result
      ansible.builtin.debug:
        var: delete_cred
'''

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        server_name=dict(type='str', required=True),
        server_username=dict(type='str', required=True),
        server_password=dict(type='str', required=True, no_log=True),
        server_port=dict(type='str', default='9419'),
        state=dict(type="str", choices=("absent", "present"), default="present"),
        id=dict(type='str', required=False),
        username=dict(type='str', required=False),
        password=dict(type='str', required=False, no_log=True),
        type=dict(type='str', choices=("Windows", "Linux", "Standard"), default='Standard'),
        description=dict(type='str', required=False),
        validate_certs=dict(type='bool', default='false')
    )

    required_if_args = [
        ["state", "present", ["username", "password"]],
        ["state", "absent", ["id"]]
    ]

    required_together_args = [
        ["password", "username"]
    ]

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
        required_if=required_if_args,
        required_together=required_together_args,
        supports_check_mode=False
    )

    # General
    apiversion = '1.1-rev0'
    state = module.params['state']
    request_server = module.params['server_name']
    request_port = module.params['server_port']

    # Authenticate
    request_username = module.params['server_username']
    request_password = module.params['server_password']
    payload = 'grant_type=password&username=' + request_username + '&password=' + request_password
    headers = {
        'accept': 'application/json',
        'x-api-version': apiversion,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    request_url = 'https://' + request_server + ':' + request_port + '/api/oauth2/token'

    method = "Post"
    login, info = fetch_url(module, request_url, headers=headers, method=method, data=payload)

    if info['status'] != 200:
        module.fail_json(msg="Fail: %s" % ("Status: " + str(info['status']) + ", Message: " + str(info['msg'])))

    try:
        login_resp = json.loads(login.read())
    except AttributeError:
        module.fail_json(msg='Parsing Response Failed', **result)

    # Payload
    if state == 'present':
        username = module.params['username']
        password = module.params['password']
        credtype = module.params['type']
        description = module.params['description']

        body = {
            'type': credtype,
            'username': username,
            'password': password,
            'description': description
        }
        bodyjson = json.dumps(body)
        headers = {
            'x-api-version': apiversion,
            'Authorization': 'Bearer ' + login_resp['access_token'],
            'Content-Type': 'application/json'
        }
        request_url = 'https://' + request_server + ':' + request_port + '/api/v1/credentials'

        method = "Post"
        req, info = fetch_url(module, request_url, headers=headers, method=method, data=bodyjson)

        if info['status'] != 201:
            module.fail_json(msg="Fail: %s" % ("Status: " + str(info['status']) + ", Message: " + str(info['msg'])))
        
        # Logout
        headers = {
            'x-api-version': apiversion,
            'Authorization': 'Bearer ' + login_resp['access_token']
        }
        request_url = 'https://' + request_server + ':' + request_port + '/api/oauth2/logout'

        method = "Post"
        logout, info = fetch_url(module, request_url, headers=headers, method=method)

        if info['status'] != 200:
            module.fail_json(msg="Fail: %s" % ("Status: " + str(info['status']) + ", Message: " + str(info['msg'])))

        # Results
        try:
            result['msg'] = json.loads(req.read())
            result['changed'] = True
        except AttributeError:
            module.fail_json(msg='Parsing Response Failed', **result)

    if state == 'absent':
        credid = module.params['id']

        headers = {
            'x-api-version': '1.0-rev1',
            'Authorization': 'Bearer ' + login_resp['access_token']
        }
        request_url = 'https://' + request_server + ':' + request_port + '/api/v1/credentials/' + credid

        method = "get"
        req, info = fetch_url(module, request_url, headers=headers, method=method)

        if info['status'] == 200:
            method = "Delete"
            req, info = fetch_url(module, request_url, headers=headers, method=method)

            if info['status'] != 204:
                module.fail_json(msg="Fail: %s" % ("Status: " + str(info['status']) + ", Message: " + str(info['msg'])))
            
            # Logout
            headers = {
                'x-api-version': apiversion,
                'Authorization': 'Bearer ' + login_resp['access_token']
            }
            request_url = 'https://' + request_server + ':' + request_port + '/api/oauth2/logout'

            method = "Post"
            logout, info = fetch_url(module, request_url, headers=headers, method=method)

            if info['status'] != 200:
                module.fail_json(msg="Fail: %s" % ("Status: " + str(info['status']) + ", Message: " + str(info['msg'])))

            # Results
            try:
                result['changed'] = True
            except AttributeError:
                module.fail_json(msg='Parsing Response Failed', **result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
