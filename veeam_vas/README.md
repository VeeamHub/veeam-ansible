# veeamhub.veeam.veeam_vas

An Ansible Role to administer the [Veeam Availability Suite](https://www.veeam.com/data-center-availability-suite.html). Here are products included in the Veeam Availability Suite:

- [Veeam Backup & Replication](https://www.veeam.com/vm-backup-recovery-replication-software.html)
- [Veeam Backup Enterprise Manager](https://www.veeam.com/backup-enterprise-manager.html)
- [Veeam ONE](https://www.veeam.com/virtualization-management-one-solution.html)

A big thanks to Markus Kraus ([@vMarkus_K](https://twitter.com/vMarkus_K))! I used his [code](https://github.com/mycloudrevolution/veeam_setup) as a starting point for this project.

- [veeamhub.veeam.veeam_vas](#veeamhubveeamveeamvas)
  - [How to use this Role](#how-to-use-this-role)
  - [Requirements](#requirements)
    - [Ansible](#ansible)
    - [OS](#os)
    - [Veeam Software](#veeam-software)
  - [Role Variables](#role-variables)
  - [Known Issues](#known-issues)
    - [General](#general)
    - [Veeam Backup & Replication](#veeam-backup--replication)
    - [Veeam Backup Enterprise Manager](#veeam-backup-enterprise-manager)
    - [Veeam ONE](#veeam-one)
  - [Example Playbooks](#example-playbooks)
    - [Veeam Backup & Replication Community Edition Install with ISO Download](#veeam-backup--replication-community-edition-install-with-iso-download)
    - [Veeam Backup & Replication Install with ISO Download](#veeam-backup--replication-install-with-iso-download)
    - [Veeam Backup & Replication Install with ISO Download and remote SQL](#veeam-backup--replication-install-with-iso-download-and-remote-sql)
    - [Veeam Backup & Replication Community Edition Install without ISO Download](#veeam-backup--replication-community-edition-install-without-iso-download)
    - [Veeam Backup & Replication Upgrade to v10](#veeam-backup--replication-upgrade-to-v10)
    - [Veeam Cloud Connect Server Upgrade to v10](#veeam-cloud-connect-server-upgrade-to-v10)
    - [Veeam Backup & Replication Patch](#veeam-backup--replication-patch)
    - [Veeam Backup Enterprise Manager Install without ISO Download](#veeam-backup-enterprise-manager-install-without-iso-download)
    - [Veeam Backup Enterprise Manager Install with ISO Download and remote SQL](#veeam-backup-enterprise-manager-install-with-iso-download-and-remote-sql)
    - [Veeam Backup Enterprise Manager Install including Cloud Connect Portal](#veeam-backup-enterprise-manager-install-including-cloud-connect-portal)
    - [Veeam Backup Enterprise Manager Upgrade to v10](#veeam-backup-enterprise-manager-upgrade-to-v10)
    - [Veeam Backup Enterprise Manager Patch](#veeam-backup-enterprise-manager-patch)
    - [Veeam ONE Install - Typical Deployment (single server)](#veeam-one-install---typical-deployment-single-server)
    - [Veeam ONE Community Edition Install - Typical Deployment (single server)](#veeam-one-community-edition-install---typical-deployment-single-server)
    - [Veeam ONE Install - Advanced Deployment (multi-server)](#veeam-one-install---advanced-deployment-multi-server)
    - [Veeam ONE Install - Typical Deployment and remote SQL](#veeam-one-install---typical-deployment-and-remote-sql)
    - [Veeam ONE Upgrade to v10](#veeam-one-upgrade-to-v10)
    - [Veeam ONE Patch](#veeam-one-patch)

## How to use this Role

This role is part of a collection of all roles in this repository. Easiest method to insatll it is using [Ansible Galaxy](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html):

`ansible-galaxy collection install veeamhub.veeam`

You can also copy the role directly from this repository and put it in your Ansible Roles folder (default: `~/.ansible/roles/`). _Note that using this method will require slight changes to the sample playbooks listed in this document._

## Requirements

Requirements listed are not complete and only include configurations tested during development and use of this Ansible Role. Keep in mind as well these requirements are in addition to Veeam's system requirements for the software to be installed/upgraded. For more information, please reference [Veeam documentation](https://www.veeam.com/documentation-guides-datasheets.html).

### Ansible

- Ansible 2.8+

### OS

- Microsoft Windows Server 2019
- Microsoft Windows Server 2016 (64-bit)

### Veeam Software

- Veeam Backup & Replication
  - 9.5 Update 4
  - 10
- Veeam Backup Enterprise Manager
  - 9.5 Update 4
  - 10
- Veeam ONE
  - 9.5 Update 4
  - 10

## Role Variables

Variables are located in two different locations:

- Default: _defaults/main.yml_
- Software-specific: _vars/_

## Known Issues

### General

- If Veeam software other than the Veeam Availability Suite is installed on the same server, this software will be taken offline during the upgrade.

### Veeam Backup & Replication

- Install/Patch/Upgrade only supports SQL authentication (no Windows auth)
  - _This is a limitation of the Ansible Role and not the Veeam Product._
- After the upgrade, any Agent-base backups (VAW, VAL) that Veeam administers will need to be upgraded.

### Veeam Backup Enterprise Manager

- Install/Patch/Upgrade only supports SQL authentication (no Windows auth)
  - _This is a limitation of the Ansible Role and not the Veeam Product._

### Veeam ONE

- Install/Patch/Upgrade only supports Windows authentication (no SQL authentication)
  - _This is a limitation of the Ansible Role and not the Veeam Product._

## Example Playbooks

Please note there are more configurations than the examples shown below. If you have any questions, please feel free to create an [issue](https://github.com/VeeamHub/veeam-ansible/issues/new/choose).

### Veeam Backup & Replication Community Edition Install with ISO Download

```yaml
- name: Veeam Backup & Replication Install
  hosts: veeam
  collections:
    - veeamhub.veeam
  tasks:
    - include_role:
        name: veeam_vas
        tasks_from: vbr_install
      vars:
        iso_download: true
        sql_install_username: "sql_install"
        sql_install_password: "ChangeM3!"
        sql_service_username: "svc_sql"
        sql_service_password: "ChangeM3!"
        sql_username: "sa"
        sql_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable
```

### Veeam Backup & Replication Install with ISO Download

```yaml
- name: Veeam Backup & Replication Install
  hosts: veeam
  collections:
    - veeamhub.veeam
  tasks:
    - include_role:
        name: veeam_vas
        tasks_from: vbr_install
      vars:
        iso_download: true
        license: true
        source_license: "/root/ansible/license.lic"
        sql_install_username: "sql_install"
        sql_install_password: "ChangeM3!"
        sql_service_username: "svc_sql"
        sql_service_password: "ChangeM3!"
        sql_username: "sa"
        sql_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable
```

### Veeam Backup & Replication Install with ISO Download and remote SQL

```yaml
- name: Veeam Backup & Replication Install with Remote SQL Server
  hosts: veeam
  collections:
    - veeamhub.veeam
  tasks:
    - include_role:
        name: veeam_vas
        tasks_from: vbr_install
      vars:
        license: true
        source_license: "/root/ansible/license.lic"
        sql_express_setup: false
        sql_instance: "sql.contoso.local"
        sql_username: "svc_veeam"
        sql_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable
```

### Veeam Backup & Replication Community Edition Install without ISO Download

```yaml
- name: Veeam Backup & Replication Install
  hosts: veeam
  collections:
    - veeamhub.veeam
  tasks:
    - include_role:
        name: veeam_vas
        tasks_from: vbr_install
      vars:
        destination: "C:\\install\\"
        destination_iso_file: "VeeamBackup&Replication_10.0.0.4461_20200401.iso"
        sql_install_username: "sql_install"
        sql_install_password: "ChangeM3!"
        sql_service_username: "svc_sql"
        sql_service_password: "ChangeM3!"
        sql_username: "sa"
        sql_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable
```

### Veeam Backup & Replication Upgrade to v10

```yaml
- name: Veeam Backup & Replication Upgrade
  hosts: veeam
  collections:
    - veeamhub.veeam
  tasks:
    - include_role:
        name: veeam_vas
        tasks_from: vbr_upgrade
      vars:
        iso_download: true
        license: true
        source_license: "/root/ansible/license.lic"
```

### Veeam Cloud Connect Server Upgrade to v10

```yaml
- name: Veeam Backup & Replication (Cloud Connect) Upgrade
  hosts: veeam
  collections:
    - veeamhub.veeam
  tasks:
    - include_role:
        name: veeam_vas
        tasks_from: vbr_upgrade
      vars:
        iso_download: true
        license: true
        source_license: "/root/ansible/license.lic"
        cloud_connect: true
```

### Veeam Backup & Replication Patch

```yaml
- name: Veeam Backup & Replication Patch
  hosts: veeam
  collections:
    - veeamhub.veeam
  tasks:
    - include_role:
        name: veeam_vas
        tasks_from: vbr_patch
      vars:
        source: "C:\\install\\"
        patch_file: "VeeamBackup&Replication_10.0.0.4461.update0.exe"
```

### Veeam Backup Enterprise Manager Install without ISO Download

```yaml
- name: Veeam Backup Enterprise Manager Install
  gather_facts: no
  hosts: veeam
  collections:
    - veeamhub.veeam
  tasks:
    - include_role:
        name: veeam_vas
        tasks_from: em_install
      vars:
        destination: "C:\\install\\"
        destination_iso_file: "VeeamBackup&Replication_10.0.0.4461_20200401.iso"
        license: true #mandatory for EM
        source_license: "/root/ansible/license.lic"
        sql_install_username: "sql_install"
        sql_install_password: "ChangeM3!"
        sql_service_username: "svc_sql"
        sql_service_password: "ChangeM3!"
        sql_username: "sa"
        sql_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable
```

### Veeam Backup Enterprise Manager Install with ISO Download and remote SQL

```yaml
- name: Veeam Backup Enterprise Manager Install
  gather_facts: no
  hosts: veeam
  collections:
    - veeamhub.veeam
  tasks:
    - include_role:
        name: veeam_vas
        tasks_from: em_install
      vars:
        iso_download: true
        license: true #mandatory for EM
        source_license: "/root/ansible/license.lic"
        sql_express_setup: false
        sql_instance: "sql.contoso.local"
        sql_username: "svc_veeam"
        sql_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable
```

### Veeam Backup Enterprise Manager Install including Cloud Connect Portal

```yaml
- name: Veeam Backup Enterprise Manager Install including Cloud Connect Portal
  gather_facts: no
  hosts: veeam
  collections:
    - veeamhub.veeam
  tasks:
    - include_role:
        name: veeam_vas
        tasks_from: em_install
      vars:
        iso_download: true
        license: true #mandatory for EM
        source_license: "/root/ansible/license.lic"
        cloud_connect: true
        sql_install_username: "sql_install"
        sql_install_password: "ChangeM3!"
        sql_service_username: "svc_sql"
        sql_service_password: "ChangeM3!"
        sql_username: "sa"
        sql_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable
```

### Veeam Backup Enterprise Manager Upgrade to v10

```yaml
- name: Backup Enterprise Manager Upgrade
  hosts: veeam
  collections:
    - veeamhub.veeam
  tasks:
    - include_role:
        name: veeam_vas
        tasks_from: em_upgrade
      vars:
        iso_download: true
        license: true
        source_license: "/root/ansible/license.lic"
        sql_instance: "sql.contoso.local"
        sql_database: "VeeamBackupReporting"
        sql_username: "sa"
        sql_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable
```

### Veeam Backup Enterprise Manager Patch

```yaml
- name: Veeam Backup Enterprise Manager Patch
  hosts: veeam
  collections:
    - veeamhub.veeam
  tasks:
    - include_role:
        name: veeam_vas
        tasks_from: em_patch
      vars:
        source: "C:\\install\\"
        patch_file: "VeeamBackup&Replication_10.0.0.4461.update0.exe"
        sql_instance: "sql.contoso.local"
        sql_database: "VeeamBackupReporting"
        sql_username: "sa"
        sql_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable
```

### Veeam ONE Install - Typical Deployment (single server)

```yaml
- name: Installing Veeam ONE Install (Typical Deployment)
  gather_facts: no
  hosts: veeam
  collections:
    - veeamhub.veeam
  vars:
    iso_download: false #this way ISO is only downloaded once
    license: true
    source_license: "/root/ansible/license.lic"
    sql_service_username: "svc_sql"
    sql_service_password: "ChangeM3!"
    one_create_service_account: true #true==local false==domain
    one_username: "svc_one"
    one_password: "ChangeM3!"
    # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable
  tasks:
    - name: Veeam ONE Server installation tasks
      include_role:
        name: veeam_vas
        tasks_from: one_server_install
      vars:
        iso_download: true #this way ISO is only downloaded once
    - name: Veeam ONE Web UI installation tasks
      include_role:
        name: veeam_vas
        tasks_from: one_web_ui_install
    - name: Veeam ONE Monitoring Client installation tasks
      include_role:
        name: veeam_vas
        tasks_from: one_client_install
```

### Veeam ONE Community Edition Install - Typical Deployment (single server)

```yaml
- name: Installing Veeam ONE Install (Typical Deployment)
  gather_facts: no
  hosts: veeam
  collections:
    - veeamhub.veeam
  vars:
    iso_download: false #this way ISO is only downloaded once
    sql_service_username: "svc_sql"
    sql_service_password: "ChangeM3!"
    one_create_service_account: true #true==local false==domain
    one_username: "svc_one"
    one_password: "ChangeM3!"
    # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable
  tasks:
    - name: Veeam ONE Server installation tasks
      include_role:
        name: veeam_vas
        tasks_from: one_server_install
      vars:
        iso_download: true #this way ISO is only downloaded once
    - name: Veeam ONE Web UI installation tasks
      include_role:
        name: veeam_vas
        tasks_from: one_web_ui_install
    - name: Veeam ONE Monitoring Client installation tasks
      include_role:
        name: veeam_vas
        tasks_from: one_client_install
```

### Veeam ONE Install - Advanced Deployment (multi-server)

```yaml
- name: Veeam ONE Advanced Deployment - Veeam ONE Server
  gather_facts: no
  hosts: server
  collections:
    - veeamhub.veeam
  tasks:
    - name: Veeam ONE Server installation tasks
      include_role:
        name: veeam_vas
        tasks_from: one_server_install
      vars:
        iso_download: true
        license: true
        source_license: "/root/ansible/license.lic"
        sql_express_setup: false
        sql_instance: "sql.contoso.local"
        one_installation_type: "1" #1-Advanced | 2-Backup data only | 3-Typical
        one_create_service_account: false #true==local false==domain
        one_username: "contoso\\jsmith"
        one_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable

- name: Veeam ONE Advanced Deployment - Veeam Web UI
  gather_facts: no
  hosts: web
  collections:
    - veeamhub.veeam
  tasks:
    - name: Veeam ONE Web UI installation tasks
      include_role:
        name: veeam_vas
        tasks_from: one_web_ui_install
      vars:
        iso_download: true
        sql_instance: "sql.contoso.local"
        one_installation_type: "1" #1-Advanced | 2-Backup data only | 3-Typical
        one_create_service_account: false #true==local false==domain
        one_username: "contoso\\jsmith"
        one_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable

- name: Veeam ONE Advanced Deployment - Monitoring Client
  gather_facts: no
  hosts: client
  collections:
    - veeamhub.veeam
  tasks:
    - name: Veeam ONE Monitoring Client installation tasks
      include_role:
        name: veeam_vas
        tasks_from: one_client_install
      vars:
        iso_download: true
        one_server: "server.contoso.local"
```

### Veeam ONE Install - Typical Deployment and remote SQL

```yaml
- name: Installing Veeam ONE Install (Typical Deployment)
  gather_facts: no
  hosts: veeam
  collections:
    - veeamhub.veeam
  vars:
    iso_download: false #this way ISO is only downloaded once
    license: true
    source_license: "/root/ansible/license.lic"
    sql_express_setup: false
    sql_instance: "sql.contoso.local"
    one_create_service_account: false #true==local false==domain
    one_username: "contoso\\jsmith"
    one_password: "ChangeM3!"
    # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable
  tasks:
    - name: Veeam ONE Server installation tasks
      include_role:
        name: veeam_vas
        tasks_from: one_server_install
      vars:
        iso_download: true #this way ISO is only downloaded once
    - name: Veeam ONE Web UI installation tasks
      include_role:
        name: veeam_vas
        tasks_from: one_web_ui_install
    - name: Veeam ONE Monitoring Client installation tasks
      include_role:
        name: veeam_vas
        tasks_from: one_client_install
```

### Veeam ONE Upgrade to v10

```yaml
- name: Veeam ONE Upgrade
  gather_facts: no
  hosts: veeam
  collections:
    - veeamhub.veeam
  vars:
    iso_download: false  #this way ISO is only downloaded once
    license: true
    source_license: "/root/ansible/license.lic"
    one_username: "svc_one"
    one_password: "ChangeM3!"
    # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable
  tasks:
    - name: Veeam ONE Server upgrade tasks
      include_role:
        name: veeam_vas
        tasks_from: one_server_upgrade
      vars:
        iso_download: true  #this way ISO is only downloaded once
    - name: Veeam ONE Web UI upgrade tasks
      include_role:
        name: veeam_vas
        tasks_from: one_web_ui_upgrade
    - name: Veeam ONE Monitoring Client upgrade tasks
      include_role:
        name: veeam_vas
        tasks_from: one_client_upgrade
    - name: Rebooting server now to complete upgrade
      win_reboot:
        msg: Reboot initiated by Ansible to complete Veeam ONE upgrade
```

### Veeam ONE Patch

```yaml
- name: Veeam Backup & Replication Patch
  hosts: veeam
  collections:
    - veeamhub.veeam
  tasks:
    - include_role:
        name: veeam_vas
        tasks_from: one_patch
      vars:
        source: "C:\\install\\"
        patch_file: "VeeamONE_9.5.4.4587_Update#4a.exe"
        one_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable
```
