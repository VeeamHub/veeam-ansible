
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



veeam_vbr_rest_credentials_info
-------------------------------

Get Veeam Backup & Replication Credentials.

..  code-block:: yaml

    - name: Test Veeam RestAPI Collection
      hosts: localhost
      gather_facts: false
      tasks:
        - name: Test veeam_vbr_servercertificate_info
          veeamhub.veeam.veeam_vbr_rest_servercertificate_info:
            server_name: "<VBR Host>"
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
            server_name: "<VBR Host>"
            server_username: "<VBR User>"
            server_password: "<VBR Password>"
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
            server_name: "<VBR Host>"
            server_username: "<VBR User>"
            server_password: "<VBR Password>"
            type: "Linux"
            username: "root"
            password: "<Password>"
            description: "Created by Ansible RestAPI Module"
          register: create_cred
        - name: Debug Result
          ansible.builtin.debug:
            var: create_cred
        - name: Test veeam_vbr_rest_credentials Delete
          veeamhub.veeam.veeam_vbr_rest_credentials:
            server_name: "<VBR Host>"
            server_username: "<VBR User>"
            server_password: "<VBR Password>"
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
            server_name: "<VBR Host>"
            server_username: "<VBR User>"
            server_password: "<VBR Password>"
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
            server_name: "<VBR Host>"
            server_username: "<VBR User>"
            server_password: "<VBR Password>"
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
            server_name: "<VBR Host>"
            server_username: "<VBR User>"
            server_password: "<VBR Password>"
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

End-to-End Create Veeam Job:

..  code-block:: yaml

    - name: Test Veeam RestAPI Collection
      hosts: localhost
      gather_facts: false
      vars:
        - repo_name: '<Repository Name>'
      tasks:
        - name: Get VBR Repos
          veeamhub.veeam.veeam_vbr_rest_repositories_info:
            server_name: "<VBR Host>"
            server_username: "<VBR User>"
            server_password: "<VBR Password>"
          register: repo_testout
        - name: Debug VBR Repos Result
          ansible.builtin.debug:
            var: repo_testout
        - name: Filter Repo Object
          ansible.builtin.set_fact:
            repo_id: "{{ repo_testout | json_query(repos_id_query) }}"
          vars:
            repos_id_query: "infrastructure_repositories.data[?name==`{{ repo_name }}`].id"
        - name: Create VBR Job
          veeamhub.veeam.veeam_vbr_rest_jobs_manage:
            server_name: "<VBR Host>"
            server_username: "<VBR User>"
            server_password: "<VBR Password>"
            state: present
            jobName: "Ansible Test"
            hostName: "<vCenter Hostname>"
            name: "<VM Name>"
            objectId: "<VM MoRef ID>"
            type: "VirtualMachine"
            description: "Created by Ansible RestAPI Module"
            backupRepositoryId: "{{ repo_id[0] }}"
          register: create_job
        - name: Debug VBR Jobs Result
          ansible.builtin.debug:
            var: create_job

End-to-End Delete Veeam Job:

..  code-block:: yaml

    - name: Test Veeam RestAPI Collection
      hosts: localhost
      gather_facts: false
      vars:
        job_name: "Ansible Test"
      tasks:
        - name: Get VBR Jobs
          veeamhub.veeam.veeam_vbr_rest_jobs_info:
            server_name: "<VBR Host>"
            server_username: "<VBR User>"
            server_password: "<VBR Password>"
          register: job_testout
        - name: Debug VBR Jobs Result
          ansible.builtin.debug:
            var: job_testout
        - name: Filter Job Object
          ansible.builtin.set_fact:
            job_id: "{{ job_testout | json_query(jobs_id_query) }}"
          vars:
            jobs_id_query: "infrastructure_jobs.data[?name==`{{ job_name }}`].id"
        - name: Delete VBR Job
          veeamhub.veeam.veeam_vbr_rest_jobs_manage:
            server_name: "<VBR Host>"
            server_username: "<VBR User>"
            server_password: "<VBR Password>"
            state: absent
            id: "{{ job_id[0] }}"
