# veeamhub.veeam.veeam_vas

An Ansible Role to administer [Veeam Backup & Replication](https://www.veeam.com/products/veeam-data-platform/backup-recovery.html) [Veeam Backup Enterprise Manager](https://www.veeam.com/products/backup-enterprise-manager.html).

Starting with version 12.1, a standalone Veeam Backup & Replication Console can now be installed & upgraded!

A big thanks to Markus Kraus ([@vMarkus_K](https://twitter.com/vMarkus_K))! I used his [code](https://github.com/mycloudrevolution/veeam_setup) as a starting point for this project.

- [veeamhub.veeam.veeam\_vas](#veeamhubveeamveeam_vas)
  - [How to use this Role](#how-to-use-this-role)
  - [Requirements](#requirements)
    - [Ansible](#ansible)
    - [OS](#os)
    - [Veeam Software](#veeam-software)
  - [Role Variables](#role-variables)
  - [Known Issues](#known-issues)
    - [General](#general)
    - [Veeam Backup \& Replication](#veeam-backup--replication)
    - [Veeam Backup Enterprise Manager](#veeam-backup-enterprise-manager)
    - [Veeam Backup \& Replication Console](#veeam-backup--replication-console)
  - [Example Playbooks](#example-playbooks)
    - [Veeam Backup \& Replication Community Edition Install with ISO Download](#veeam-backup--replication-community-edition-install-with-iso-download)
    - [Veeam Backup \& Replication Community Edition Install with ISO Download](#veeam-backup--replication-community-edition-install-with-iso-download-1)
    - [Veeam Backup \& Replication Install with ISO Download](#veeam-backup--replication-install-with-iso-download)
    - [Veeam Backup \& Replication Install with ISO Download and remote Microsoft SQL](#veeam-backup--replication-install-with-iso-download-and-remote-microsoft-sql)
    - [Veeam Backup \& Replication Install with ISO Download and remote PostgreSQL](#veeam-backup--replication-install-with-iso-download-and-remote-postgresql)
    - [Veeam Backup \& Replication Upgrade](#veeam-backup--replication-upgrade)
    - [Veeam Cloud Connect Server Upgrade](#veeam-cloud-connect-server-upgrade)
    - [Veeam Backup \& Replication Patch](#veeam-backup--replication-patch)
    - [Veeam Backup Enterprise Manager Install without ISO Download](#veeam-backup-enterprise-manager-install-without-iso-download)
    - [Veeam Backup Enterprise Manager Install with ISO Download and remote Microsoft SQL](#veeam-backup-enterprise-manager-install-with-iso-download-and-remote-microsoft-sql)
    - [Veeam Backup Enterprise Manager Install with ISO Download and remote PostgreSQL](#veeam-backup-enterprise-manager-install-with-iso-download-and-remote-postgresql)
    - [Veeam Backup Enterprise Manager Upgrade](#veeam-backup-enterprise-manager-upgrade)
    - [Veeam Backup Enterprise Manager Patch](#veeam-backup-enterprise-manager-patch)
    - [Veeam Backup \& Replication Console Install](#veeam-backup--replication-console-install)
    - [Veeam Backup \& Replication Console Install without ISO download](#veeam-backup--replication-console-install-without-iso-download)
    - [Veeam Backup \& Replication Console Upgrade](#veeam-backup--replication-console-upgrade)

## How to use this Role

This role is part of a [collection](https://galaxy.ansible.com/veeamhub/veeam) of all roles in this repository. Easiest method to insatll it is using [Ansible Galaxy](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html):

```bash
ansible-galaxy collection install veeamhub.veeam
```

## Requirements

Requirements listed are not complete and only include configurations tested during development and use of this Ansible Role. Keep in mind as well these requirements are in addition to Veeam's system requirements for the software to be installed/upgraded. For more information, please reference [Veeam documentation](https://www.veeam.com/documentation-guides-datasheets.html).

This collection depends on Windows modules (`ansible.windows` & `community.windows`) that are not standard in Ansible anymore (2.10.x). If the collection is installed using the Ansible Galaxy CLI (see previous section), no further action is required on your part.

### Ansible

- Ansible 2.16+

### OS

- Microsoft Windows Server 2025
- Microsoft Windows Server 2022
- Microsoft Windows Server 2019

### Veeam Software

- Veeam Backup & Replication
  - 12
  - 13
- Veeam Backup Enterprise Manager
  - 12
  - 13

## Role Variables

Variables are located in two different locations:

- Default: _defaults/main.yml_
- Software-specific: _vars/_

## Known Issues

### General

- If Veeam software other than the Veeam Backup & Replication and Veeam Backup Enterprise Manager is installed on the same server, this software will be taken offline during the upgrade.

### Veeam Backup & Replication

- Starting with v13, PowerShell 7 is used for Veeam cmdlets. Ansible is still catching up so modules in this collection do not support v13. For more information see [here](https://github.com/VeeamHub/veeam-ansible/issues/83).
- Starting with v12, PostgreSQL is installed instead of SQL Express.
- If a remote PostgreSQL database is chosen, performance tuning needs to be applied. The new `veeam_vbr_set_postgres_database_server_limits` module hosted in this collection can assist in this regard.
  - [Check out the sample playbook below](#Veeam-Backup--Replication-Install-with-ISO-Download-and-remote-PostgreSQL-v12)

### Veeam Backup Enterprise Manager

- Starting with v12, PostgreSQL is installed instead of SQL Express.
- If a remote PostgreSQL database is chosen, performance tuning needs to be applied. The new `veeam_vbr_set_postgres_database_server_limits` module hosted in this collection can assist in this regard.

### Veeam Backup & Replication Console

- Install/Upgrade only available for versions 12.3 and later

## Example Playbooks

Please note there are more configurations than the examples shown below. If you have any questions, please feel free to create an [issue](https://github.com/VeeamHub/veeam-ansible/issues/new/choose).

### Veeam Backup & Replication Community Edition Install with ISO Download

```yaml
- name: Veeam Backup & Replication Install
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: vbr_install
      vars:
        version: "13"
        iso_download: true
```

### Veeam Backup & Replication Community Edition Install with ISO Download

```yaml
- name: Veeam Backup & Replication Install
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: vbr_install
      vars:
        version: "13"
        iso_download: true
        sql_install_username: "sql_install"
        sql_install_password: "ChangeM3!"
        sql_service_username: "svc_sql"
        sql_service_password: "ChangeM3!"
        sql_username: "postgres"
        sql_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/vault_guide/vault_encrypting_content.html#creating-encrypted-variables
```

### Veeam Backup & Replication Install with ISO Download

```yaml
- name: Veeam Backup & Replication Install
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: vbr_install
      vars:
        version: "13"
        iso_download: true
        license: true
        source_license: "/root/ansible/license.lic"
```

### Veeam Backup & Replication Install with ISO Download and remote Microsoft SQL

```yaml
- name: Veeam Backup & Replication Install with Remote Microsoft SQL Server
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: vbr_install
      vars:
        version: "13"
        license: true
        source_license: "/root/ansible/license.lic"
        sql_express_setup: false
        sql_engine: "0" # 0-MSSQL / 1-Postgres (default)
        sql_authentication: "1" # 0-Windows (default) 1-Native
        sql_instance: "sql.contoso.local"
        sql_username: "svc_veeam"
        sql_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/vault_guide/vault_encrypting_content.html#creating-encrypted-variables
```

### Veeam Backup & Replication Install with ISO Download and remote PostgreSQL

```yaml
- name: Veeam Backup & Replication Install with Remote PostgreSQL Server
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: vbr_install
      vars:
        version: "13"
        license: true
        source_license: "/root/ansible/license.lic"
        sql_express_setup: false
        sql_authentication: "1" # 0-Windows (default) 1-Native
        sql_instance: "sql.contoso.local"
        sql_username: "svc_veeam"
        sql_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/vault_guide/vault_encrypting_content.html#creating-encrypted-variables
    - name: Applying tuning on a remote PostgreSQL server running as the VBR DB
       veeamhub.veeam.veeam_vbr_set_postgres_database_server_limits:
         os_type: Windows
         cpu_count: 16
         ram_gb: 30
```

### Veeam Backup & Replication Upgrade

```yaml
- name: Veeam Backup & Replication Upgrade
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: vbr_upgrade
      vars:
        version: "13"
        iso_download: true
        license: true
        source_license: "/root/ansible/license.lic"
```

### Veeam Cloud Connect Server Upgrade

```yaml
- name: Veeam Backup & Replication (Cloud Connect) Upgrade
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: vbr_upgrade
      vars:
        version: "13"
        iso_download: true
        license: true
        source_license: "/root/ansible/license.lic"
        cloud_connect: true
```

### Veeam Backup & Replication Patch

```yaml
- name: Veeam Backup & Replication Patch
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: vbr_patch
      vars:
        source: "C:\\install\\"
        patch_file: "VeeamBackup&Replication_12.3.2.4165_20251014_patch.exe"
```

### Veeam Backup Enterprise Manager Install without ISO Download

```yaml
- name: Veeam Backup Enterprise Manager Install
  gather_facts: false
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: em_install
      vars:
        version: "13"
        destination: "C:\\install\\"
        destination_iso_file: "VeeamBackup&Replication_13.0.1.180_20251114.iso"
        license: true #mandatory for EM
        source_license: "/root/ansible/license.lic"
```

### Veeam Backup Enterprise Manager Install with ISO Download and remote Microsoft SQL

```yaml
- name: Veeam Backup Enterprise Manager Install
  gather_facts: false
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: em_install
      vars:
        version: "13"
        iso_download: true
        license: true #mandatory for EM
        source_license: "/root/ansible/license.lic"
        sql_express_setup: false
        sql_engine: "0" # 0-MSSQL / 1-Postgres (default)
        sql_authentication: "1" # 0-Windows (default) 1-Native
        sql_instance: "sql.contoso.local"
        sql_username: "svc_veeam"
        sql_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/vault_guide/vault_encrypting_content.html#creating-encrypted-variables
```

### Veeam Backup Enterprise Manager Install with ISO Download and remote PostgreSQL

```yaml
- name: Veeam Backup Enterprise Manager Install
  gather_facts: false
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: em_install
      vars:
        version: "13"
        iso_download: true
        license: true #mandatory for EM
        source_license: "/root/ansible/license.lic"
        sql_express_setup: false
        sql_authentication: "1" # 0-Windows (default) 1-Native
        sql_instance: "sql.contoso.local"
        sql_username: "svc_veeam"
        sql_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/vault_guide/vault_encrypting_content.html#creating-encrypted-variables
```

### Veeam Backup Enterprise Manager Upgrade

```yaml
- name: Backup Enterprise Manager Upgrade
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: em_upgrade
      vars:
        version: "13"
        iso_download: true
        license: true
        source_license: "/root/ansible/license.lic"
```

### Veeam Backup Enterprise Manager Patch

```yaml
- name: Veeam Backup Enterprise Manager Patch
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: em_patch
      vars:
        source: "C:\\install\\"
        patch_file: "VeeamBackup&Replication_12.3.2.4165_20251014_patch.exe"
        sql_instance: "sql.contoso.local"
        sql_database: "VeeamBackupReporting"
        sql_username: "sa"
        sql_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/vault_guide/vault_encrypting_content.html#creating-encrypted-variables
```

### Veeam Backup & Replication Console Install

```yaml
- name: Veeam Backup & Replication Console Install
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: vbr_console_install
      vars:
        version: "13"
        iso_download: true
```

### Veeam Backup & Replication Console Install without ISO download

```yaml
- name: Veeam Backup & Replication Console Install
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: vbr_console_install
      vars:
        version: "13"
        destination: "C:\\install\\"
        destination_iso_file: "VeeamBackup&Replication_13.0.1.180_20251114.iso"
```

### Veeam Backup & Replication Console Upgrade

```yaml
- name: Veeam Backup & Replication Console Upgrade
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: vbr_console_upgrade
      vars:
        version: "13"
        iso_download: true
```
