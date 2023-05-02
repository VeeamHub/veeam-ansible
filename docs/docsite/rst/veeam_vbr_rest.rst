
..
  Copyright: (c) 2022, Markus Kraus <markus.kraus@gmail.com>
  GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

.. _ansible_collections.veeamhub.veeam.docsite.veeam_vbr_rest:

Veeam Backup & Replication RestAPI Modules
==========================================

.. contents::
   :local:
   :depth: 1


veeam_vbr_rest_servercertificate_info
-------------------------------------

Get Current Veeam Backup Server Certificate from RestAPI.

..  code-block:: yaml

    - name: Test Veeam RestAPI Collection
      hosts: localhost
      gather_facts: false
      tasks:
      - name: Test veeam_vbr_servercertificate_info
        veeamhub.veeam.veeam_vbr_rest_servercertificate_info:
            server_name: '<VBR Host>'
        register: testout
      - name: Debug Result
        ansible.builtin.debug:
            var: testout

veeam_vbr_rest_credentials_info
-------------------------------

Get Veeam Backup & Replication Credentials.

..  code-block:: yaml

    - name: Test Veeam RestAPI Collection
      hosts: localhost
      gather_facts: false
      tasks:
      - name: Test veeam_vbr_credentials_info
        veeamhub.veeam.veeam_vbr_rest_credentials_info:
            server_name: '<VBR Host>'
            server_username: '<VBR User>'
            server_password: '<VBR Password>'
        register: testout
      - name: Debug Result
        ansible.builtin.debug:
            var: testout

veeam_vbr_rest_cloudcredentials_info
------------------------------------

Get Veeam Backup & Replication Cloud Credentials.

..  code-block:: yaml

    - name: Test Veeam RestAPI Collection
      hosts: localhost
      gather_facts: false
      tasks:
      - name: Test veeam_vbr_cloudcredentials_info
        veeamhub.veeam.veeam_vbr_rest_cloudcredentials_info:
            server_name: '<VBR Host>'
            server_username: '<VBR User>'
            server_password: '<VBR Password>'
        register: testout
      - name: Debug Result
        ansible.builtin.debug:
            var: testout

veeam_vbr_rest_credentials
--------------------------

Add and Remove Veeam Backup & Replication Credentials.

**Please note** This is an MVP with very limited functionality

Known Limitations:

- Not idempotent

..  code-block:: yaml

    - name: Test Veeam RestAPI Collection
      hosts: localhost
      gather_facts: false
      tasks:
      - name: Test veeam_vbr_rest_credentials Create
        veeamhub.veeam.veeam_vbr_rest_credentials:
            server_name: '<VBR Host>'
            server_username: '<VBR User>'
            server_password: '<VBR Password>'
            type: 'Linux'
            username: 'root'
            password: '<Password>'
            description: 'Created by Ansible RestAPI Module'
        register: create_cred
      - name: Debug Result
        ansible.builtin.debug:
            var: create_cred
      - name: Test veeam_vbr_rest_credentials Delete
        veeamhub.veeam.veeam_vbr_rest_credentials:
            server_name: '<VBR Host>'
            server_username: '<VBR User>'
            server_password: '<VBR Password>'
            id: "{{ create_cred.msg.id }}"
            state: absent
        register: delete_cred
      - name: Debug Result
        ansible.builtin.debug:
            var: delete_cred

veeam_vbr_rest_repositories_info
--------------------------------

Get Veeam Backup & Replication Repositories.

**Please note** This is an MVP with very limited functionality

Known Limitations:

- No SOBR listing

..  code-block:: yaml

    - name: Test Veeam RestAPI Collection
      hosts: localhost
      gather_facts: false
      tasks:
      - name: Test veeam_vbr_rest_epositories_info
        veeamhub.veeam.veeam_vbr_rest_repositories_info:
            server_name: '<VBR Host>'
            server_username: '<VBR User>'
            server_password: '<VBR Password>'
        register: testout
      - name: Debug Result
        ansible.builtin.debug:
            var: testout

veeam_vbr_rest_managedservers_info
----------------------------------

Get Veeam Backup & Replication Managed Servers.

..  code-block:: yaml

    - name: Test Veeam RestAPI Collection
      hosts: localhost
      gather_facts: false
      tasks:
      - name: Test veeam_vbr_rest_managedservers_info
        veeamhub.veeam.veeam_vbr_rest_managedservers_info:
            server_name: '<VBR Host>'
            server_username: '<VBR User>'
            server_password: '<VBR Password>'
        register: testout
      - name: Debug Result
        ansible.builtin.debug:
            var: testout

veeam_vbr_rest_jobs_info
------------------------

Get Veeam Backup & Replication Jobs.

..  code-block:: yaml

    - name: Test Veeam RestAPI Collection
      hosts: localhost
      gather_facts: false
      tasks:
      - name: Get VBR Jobs
        veeamhub.veeam.veeam_vbr_rest_jobs_info:
            server_name: '<VBR Host>'
            server_username: '<VBR User>'
            server_password: '<VBR Password>'
        register: job_testout
      - name: Debug VBR Jobs Result
        ansible.builtin.debug:
            var: job_testout

veeam_vbr_rest_jobs_manage
--------------------------

Add and Delete Veeam Backup & Replication Jobs.

**Please note** This is an MVP with very limited functionality

Known Limitations:

- Only vSphere Jobs with a single VM
- Not idempotent
- No Options

End-to-End Create Veeam Job and vSphere VM:

..  code-block:: yaml

    - name: Test Veeam RestAPI Collection
      hosts: localhost
      gather_facts: false
      vars:
        repos_query: "infrastructure_repositories.data[?name=='Local01']"
        vcenter_hostname: "<vCenter Host>"
        vcenter_username: "<vCenter User>"
        vcenter_password: "<vCenter Password>"
        vm_datacenter: "<vCenter DC>"
        vm_cluster: "<vCenter Cluster>"
        vm_name: "Ansible_Test"
        vm_folder: "<vCenter Folder>"
        vm_datastore: "<Datastore Name>"
        vm_network: "<Network Name>"
      tasks:
      - name: Create vSphere VM {{ vm_name }}
        community.vmware.vmware_guest:
            hostname: "{{ vcenter_hostname }}"
            username: "{{ vcenter_username }}"
            password: "{{ vcenter_password }}"
            validate_certs: yes
            datacenter: "{{ vm_datacenter }}"
            cluster: "{{ vm_cluster }}"
            folder: "{{ vm_folder }}"
            name: "{{ vm_name }}" 
            state: poweredoff
            guest_id: "rhel8_64Guest"
            datastore: "{{ vm_datastore }}"
            disk:
              - size_gb: "16"
            hardware:
                version: 19
                memory_mb: 2048
                memory_reservation_lock: false
                num_cpus: 1
                scsi: paravirtual
                boot_firmware: efi
            networks:
              - name: "{{ vm_network }}"
                device_type: vmxnet3
            advanced_settings:
              - key: "ctkEnabled"
                value: "True"
            wait_for_ip_address: no
        register: deploy_vm
      - name: VBR API-Test
        veeamhub.veeam.veeam_vbr_rest_servercertificate_info:
            server_name: '<VBR Host>'
        register: api_testout
      - name: Debug VBR API-Test Result
        ansible.builtin.debug:
            var: api_testout
      - name: Get VBR Repos
        veeamhub.veeam.veeam_vbr_rest_repositories_info:
            server_name: '<VBR Host>'
            server_username: '<VBR User>'
            server_password: '<VBR Password>'
        register: repo_testout
      - name: Debug VBR Repos Result
        ansible.builtin.debug:
            var: repo_testout | json_query(repos_query)
      - name: Filter Repo Object
        set_fact: 
          repo_id: "{{ repo_testout | json_query(repos_id_query) }}"
        vars:
          repos_id_query: 'infrastructure_repositories.data[?name==`Local01`].id'
      - name: Create VBR Job
        veeamhub.veeam.veeam_vbr_rest_jobs_manage:
            server_name: '<VBR Host>'
            server_username: '<VBR User>'
            server_password: '<VBR Password>'
            state: present
            jobName: 'Ansible Test'
            hostName: "{{ vcenter_hostname }}"
            name: "{{ vm_name }}"
            objectId: "{{ deploy_vm.instance.moid }}"
            type: 'VirtualMachine'
            description: 'My Test'
            backupRepositoryId: "{{ repo_id[0] }}"
        register: job_createout
      - name: Debug VBR Jobs Result
        ansible.builtin.debug:
            var: job_createout

End-to-End Delete Veeam Job and vSphere VM:

..  code-block:: yaml

    - name: Test Veeam RestAPI Collection
      hosts: localhost
      gather_facts: false
      vars:
        jobs_query: "infrastructure_jobs.data[?name=='Ansible Test']"
        vcenter_hostname: "<vCenter Host>"
        vcenter_username: "<vCenter User>"
        vcenter_password: "<vCenter Password>"
        vm_datacenter: "<vCenter DC>"
        vm_cluster: "<vCenter Cluster>"
        vm_name: "Ansible_Test"
        vm_folder: "<vCenter Folder>"
      tasks:
      - name: Delete vSphere VM {{ vm_name }}
        community.vmware.vmware_guest:
            hostname: "{{ vcenter_hostname }}"
            username: "{{ vcenter_username }}"
            password: "{{ vcenter_password }}"
            validate_certs: yes
            datacenter: "{{ vm_datacenter }}"
            cluster: "{{ vm_cluster }}"
            folder: "{{ vm_folder }}"
            name: "{{ vm_name }}" 
            state: absent
        register: Delete_vm
      - name: Get VBR Jobs
        veeamhub.veeam.veeam_vbr_rest_jobs_info:
            server_name: '<VBR Host>'
            server_username: '<VBR User>'
            server_password: '<VBR Password>'
        register: job_testout
      - name: Debug VBR Jobs Result
        ansible.builtin.debug:
            var: job_testout | json_query(jobs_query)
      - name: Filter Job Object
        set_fact: 
          job_id: "{{ job_testout | json_query(jobs_id_query) }}"
        vars:
          jobs_id_query: 'infrastructure_jobs.data[?name==`Ansible Test`].id'
      - name: Delete VBR Job
        veeamhub.veeam.veeam_vbr_rest_jobs_manage:
            server_name: '<VBR Host>'
            server_username: '<VBR User>'
            server_password: '<VBR Password>'
            state: absent
            id: "{{ job_id[0] }}"
