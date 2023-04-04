#!/usr/bin/python

# Copyright: (c) 2020, Your Name <YourName@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url

DOCUMENTATION = r'''
# Pass in a message

'''

EXAMPLES = r'''
# Pass in a message

'''

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        server_name=dict(type='str', required=True),
        server_username=dict(type='str', required=True),
        server_password=dict(type='str', required=True, no_log=True),
        server_port=dict(type='str', default='9419'),
        validate_certs=dict(type='bool', default='false')
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
    apiversion = '1.0-rev2'

    # Authenticate
    request_server = module.params['server_name']
    request_port = module.params['server_port']
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
    headers = {
        'x-api-version': apiversion,
        'Authorization': 'Bearer ' + login_resp['access_token']
    }
    request_url = 'https://' + request_server + ':' + request_port + '/api/v1/jobs'

    method = "Get"
    req, info = fetch_url(module, request_url, headers=headers, method=method)

    if info['status'] != 200:
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
        result['infrastructure_jobs'] = json.loads(req.read())
    except AttributeError:
        module.fail_json(msg='Parsing Response Failed', **result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
