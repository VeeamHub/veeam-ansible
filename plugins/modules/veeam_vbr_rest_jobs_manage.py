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
        state=dict(type="str", choices=("absent", "present"), default="present"),
        id=dict(type='str', required=False),
        jobName=dict(type='str', required=False),
        hostName=dict(type='str', required=False),
        name=dict(type='str', required=False),
        objectId=dict(type='str', required=False),
        type=dict(type='str', choices=("VirtualMachine", "vCenterServer"), default="VirtualMachine"),
        backupRepositoryId=dict(type='str', required=False),
        description=dict(type='str', required=False),
        validate_certs=dict(type='bool', default='false')
    )

    required_if_args = [
        ["state", "present", ["jobName", "hostName", "name", "objectId", "backupRepositoryId"]],
        ["state", "absent", ["id"]]
    ]

    required_together_args = [
        ["jobName", "hostName", "name", "objectId", "backupRepositoryId"]
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
    apiversion = '1.0-rev2'
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
        jobName = module.params['jobName']
        type = module.params['type']
        hostName = module.params['hostName']
        name = module.params['name']
        objectId = module.params['objectId']
        description = module.params['description']
        backupRepositoryId = module.params['backupRepositoryId']

        body = {
            "name": jobName,
            "description": description,
            "type": "Backup",
            "isHighPriority": "false",
            "virtualMachines": {
                "includes": [
                {
                    "hostName": hostName,
                    "name": name,
                    "type": type,
                    "objectId": objectId
                }
                ]
            },
            "storage": {
                "backupRepositoryId": backupRepositoryId,
                "backupProxies": {
                "autoSelection": "true",
                "proxyIds": [ ]
                },
                "retentionPolicy": {
                "type": "Days",
                "quantity": 7
                }
            },
            "guestProcessing": {
                "appAwareProcessing": {
                    "isEnabled": "false",
                    "appSettings": []
                },
                "guestFSIndexing": {
                    "isEnabled": "false",
                    "indexingSettings": []
                },
                "guestInteractionProxies": {
                    "autoSelection": "true",
                    "proxyIds": []
                },
                "guestCredentials": {
                    "credsType": "Linux",
                    "credsId": "00000000-0000-0000-0000-000000000000",
                    "credentialsPerMachine": []
                }
            },
            "schedule": {
                "runAutomatically": "false",
                "daily": {
                    "dailyKind": "Everyday",
                    "isEnabled": "true",
                    "localTime": "22:00",
                    "days": [
                        "sunday",
                        "monday",
                        "tuesday",
                        "wednesday",
                        "thursday",
                        "friday",
                        "saturday"
                    ]
                },
                "monthly": {
                    "dayOfWeek": "saturday",
                    "dayNumberInMonth": "Fourth",
                    "isEnabled": "false",
                    "localTime": "22:00",
                    "dayOfMonth": 1,
                    "months": [
                        "January",
                        "February",
                        "March",
                        "April",
                        "May",
                        "June",
                        "July",
                        "August",
                        "September",
                        "October",
                        "November",
                        "December"
                    ]
                },
                "periodically": {
                    "periodicallyKind": "Hours",
                    "isEnabled": "false",
                    "frequency": 1,
                    "backupWindow": {
                        "days": [
                            {
                                "day": "sunday",
                                "hours": "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1"
                            },
                            {
                                "day": "monday",
                                "hours": "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1"
                            },
                            {
                                "day": "tuesday",
                                "hours": "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1"
                            },
                            {
                                "day": "wednesday",
                                "hours": "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1"
                            },
                            {
                                "day": "thursday",
                                "hours": "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1"
                            },
                            {
                                "day": "friday",
                                "hours": "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1"
                            },
                            {
                                "day": "saturday",
                                "hours": "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1"
                            }
                        ]
                    },
                    "startTimeWithinAnHour": 0
                },
                "continuously": {
                    "isEnabled": "false",
                    "backupWindow": {
                        "days": [
                            {
                                "day": "sunday",
                                "hours": "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1"
                            },
                            {
                                "day": "monday",
                                "hours": "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1"
                            },
                            {
                                "day": "tuesday",
                                "hours": "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1"
                            },
                            {
                                "day": "wednesday",
                                "hours": "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1"
                            },
                            {
                                "day": "thursday",
                                "hours": "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1"
                            },
                            {
                                "day": "friday",
                                "hours": "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1"
                            },
                            {
                                "day": "saturday",
                                "hours": "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1"
                            }
                        ]
                    }
                },
                "afterThisJob": {
                    "isEnabled": "false",
                    "jobName": ""
                },
                "retry": {
                    "isEnabled": "true",
                    "retryCount": 3,
                    "awaitMinutes": 10
                },
                "backupWindow": {
                    "isEnabled": "false",
                    "backupWindow": {
                        "days": [
                            {
                                "day": "sunday",
                                "hours": "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1"
                            },
                            {
                                "day": "monday",
                                "hours": "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1"
                            },
                            {
                                "day": "tuesday",
                                "hours": "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1"
                            },
                            {
                                "day": "wednesday",
                                "hours": "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1"
                            },
                            {
                                "day": "thursday",
                                "hours": "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1"
                            },
                            {
                                "day": "friday",
                                "hours": "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1"
                            },
                            {
                                "day": "saturday",
                                "hours": "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1"
                            }
                        ]
                    }
                }
            }
        }
        bodyjson = json.dumps(body)
        headers = {
            'x-api-version': apiversion,
            'Authorization': 'Bearer ' + login_resp['access_token'],
            'Content-Type': 'application/json'
        }
        request_url = 'https://' + request_server + ':' + request_port + '/api/v1/jobs'

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
        id = module.params['id']

        headers = {
            'x-api-version': '1.0-rev1',
            'Authorization': 'Bearer ' + login_resp['access_token']
        }
        request_url = 'https://' + request_server + ':' + request_port + '/api/v1/jobs/' + id

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
