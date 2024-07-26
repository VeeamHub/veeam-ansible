# veeamhub.veeam.veeam_vas

An Ansible Role to administer the [Veeam Availability Suite](https://www.veeam.com/data-center-availability-suite.html). Here are products included in the Veeam Availability Suite:

- [Veeam Backup & Replication](https://www.veeam.com/vm-backup-recovery-replication-software.html)
- [Veeam Backup Enterprise Manager](https://www.veeam.com/backup-enterprise-manager.html)
- [Veeam ONE](https://www.veeam.com/virtualization-management-one-solution.html)

Starting with version 12.1, the Veeam Backup & Replication Console can now be installed & upgraded!

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
    - [Veeam ONE](#veeam-one)
  - [Example Playbooks](#example-playbooks)
    - [Veeam Backup \& Replication Community Edition Install with ISO Download (v12.1+)](#veeam-backup--replication-community-edition-install-with-iso-download-v121)
    - [Veeam Backup \& Replication Community Edition Install with ISO Download (v12)](#veeam-backup--replication-community-edition-install-with-iso-download-v12)
    - [Veeam Backup \& Replication Community Edition Install with ISO Download (v11-)](#veeam-backup--replication-community-edition-install-with-iso-download-v11-)
    - [Veeam Backup \& Replication Install with ISO Download (v12.1+)](#veeam-backup--replication-install-with-iso-download-v121)
    - [Veeam Backup \& Replication Install with ISO Download (v12-)](#veeam-backup--replication-install-with-iso-download-v12-)
    - [Veeam Backup \& Replication Install with ISO Download and remote Microsoft SQL (v12.1+)](#veeam-backup--replication-install-with-iso-download-and-remote-microsoft-sql-v121)
    - [Veeam Backup \& Replication Install with ISO Download and remote PostgreSQL (v12.1+)](#veeam-backup--replication-install-with-iso-download-and-remote-postgresql-v121)
    - [Veeam Backup \& Replication Install with ISO Download and remote Microsoft SQL (v12)](#veeam-backup--replication-install-with-iso-download-and-remote-microsoft-sql-v12)
    - [Veeam Backup \& Replication Install with ISO Download and remote PostgreSQL (v12)](#veeam-backup--replication-install-with-iso-download-and-remote-postgresql-v12)
    - [Veeam Backup \& Replication Install with ISO Download and remote SQL (v11-)](#veeam-backup--replication-install-with-iso-download-and-remote-sql-v11-)
    - [Veeam Backup \& Replication Community Edition Install without ISO Download](#veeam-backup--replication-community-edition-install-without-iso-download)
    - [Veeam Backup \& Replication Upgrade - Native Auth (v12.1+)](#veeam-backup--replication-upgrade---native-auth-v121)
    - [Veeam Backup \& Replication Upgrade - Windows Auth (v12.1+)](#veeam-backup--replication-upgrade---windows-auth-v121)
    - [Veeam Backup \& Replication Upgrade (v12-)](#veeam-backup--replication-upgrade-v12-)
    - [Veeam Cloud Connect Server Upgrade](#veeam-cloud-connect-server-upgrade)
    - [Veeam Backup \& Replication Patch](#veeam-backup--replication-patch)
    - [Veeam Backup Enterprise Manager Install without ISO Download (v12.1+)](#veeam-backup-enterprise-manager-install-without-iso-download-v121)
    - [Veeam Backup Enterprise Manager Install without ISO Download (v12-)](#veeam-backup-enterprise-manager-install-without-iso-download-v12-)
    - [Veeam Backup Enterprise Manager Install with ISO Download and remote Microsoft SQL (v12.1+)](#veeam-backup-enterprise-manager-install-with-iso-download-and-remote-microsoft-sql-v121)
    - [Veeam Backup Enterprise Manager Install with ISO Download and remote PostgreSQL (v12.1+)](#veeam-backup-enterprise-manager-install-with-iso-download-and-remote-postgresql-v121)
    - [Veeam Backup Enterprise Manager Install with ISO Download and remote Microsoft SQL (v12)](#veeam-backup-enterprise-manager-install-with-iso-download-and-remote-microsoft-sql-v12)
    - [Veeam Backup Enterprise Manager Install with ISO Download and remote PostgreSQL (v12)](#veeam-backup-enterprise-manager-install-with-iso-download-and-remote-postgresql-v12)
    - [Veeam Backup Enterprise Manager Install with ISO Download and remote SQL (v11-)](#veeam-backup-enterprise-manager-install-with-iso-download-and-remote-sql-v11-)
    - [Veeam Backup Enterprise Manager Install including Cloud Connect Portal](#veeam-backup-enterprise-manager-install-including-cloud-connect-portal)
    - [Veeam Backup Enterprise Manager Upgrade - Native Auth (v12.1+)](#veeam-backup-enterprise-manager-upgrade---native-auth-v121)
    - [Veeam Backup Enterprise Manager Upgrade - Windows Auth (v12.1+)](#veeam-backup-enterprise-manager-upgrade---windows-auth-v121)
    - [Veeam Backup Enterprise Manager Upgrade (v12-)](#veeam-backup-enterprise-manager-upgrade-v12-)
    - [Veeam Backup Enterprise Manager Patch](#veeam-backup-enterprise-manager-patch)
    - [Veeam Backup \& Replication Console Install](#veeam-backup--replication-console-install)
    - [Veeam Backup \& Replication Console Install without ISO download](#veeam-backup--replication-console-install-without-iso-download)
    - [Veeam Backup \& Replication Console Upgrade](#veeam-backup--replication-console-upgrade)
    - [Veeam ONE Install - Typical Deployment (single server)](#veeam-one-install---typical-deployment-single-server)
    - [Veeam ONE Community Edition Install - Typical Deployment (single server)](#veeam-one-community-edition-install---typical-deployment-single-server)
    - [Veeam ONE Install - Advanced Deployment (multi-server)](#veeam-one-install---advanced-deployment-multi-server)
    - [Veeam ONE Install - Typical Deployment and remote SQL](#veeam-one-install---typical-deployment-and-remote-sql)
    - [Veeam ONE Typical Upgrade](#veeam-one-typical-upgrade)
    - [Veeam ONE Upgrade - Advanced Deployment (multi-server)](#veeam-one-upgrade---advanced-deployment-multi-server)
    - [Veeam ONE Patch](#veeam-one-patch)

## How to use this Role

This role is part of a [collection](https://galaxy.ansible.com/veeamhub/veeam) of all roles in this repository. Easiest method to insatll it is using [Ansible Galaxy](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html):

```bash
ansible-galaxy collection install veeamhub.veeam
```

## Requirements

Requirements listed are not complete and only include configurations tested during development and use of this Ansible Role. Keep in mind as well these requirements are in addition to Veeam's system requirements for the software to be installed/upgraded. For more information, please reference [Veeam documentation](https://www.veeam.com/documentation-guides-datasheets.html).

This collection depends on Windows modules (`ansible.windows` & `community.windows`) that are not standard in Ansible anymore (2.10.x). If the collection is installed using the Ansible Galaxy CLI (see previous section), no further action is required on your part.

### Ansible

- Ansible 2.14+

### OS

- Microsoft Windows Server 2022
- Microsoft Windows Server 2019

### Veeam Software

- Veeam Backup & Replication
  - 11
  - 12
- Veeam Backup Enterprise Manager
  - 11
  - 12
- Veeam ONE
  - 11
  - 12

## Role Variables

Variables are located in two different locations:

- Default: _defaults/main.yml_
- Software-specific: _vars/_

## Known Issues

### General

- If Veeam software other than the Veeam Availability Suite is installed on the same server, this software will be taken offline during the upgrade.

### Veeam Backup & Replication

- Install/Patch/Upgrade only supports SQL authentication (no Windows auth)
  - _Both Windows & Native SQL authentication are accepted for versions 12.1 and later._
- Starting with v12, PostgreSQL is installed instead of SQL Express.
- If a remote PostgreSQL database is chosen, performance tuning needs to be applied. The new `veeam_vbr_set_postgres_database_server_limits` module hosted in this collection can assist in this regard.
  - [Check out the sample playbook below](#Veeam-Backup--Replication-Install-with-ISO-Download-and-remote-PostgreSQL-v12)
- After the upgrade, Veeam Agents (VAW, VAL) will need to be upgraded.
- Optional plug-ins (see below) are not currently included in this collection
  - _These plugins are now included for versions 12.1 and later._
  - AWS Plug-in for Veeam Backup & Replication
  - Microsoft Azure Plug-in for Veeam Backup & Replication
  - Google Cloud Platform Plug-in for Veeam Backup & Replication
  - Veeam Backup for Nutanix AHV

### Veeam Backup Enterprise Manager

- Install/Patch/Upgrade only supports SQL authentication (no Windows auth)
  - _Both Windows & Native SQL authentication are accepted for versions 12.1 and later._
- Starting with v12, PostgreSQL is installed instead of SQL Express.
- If a remote PostgreSQL database is chosen, performance tuning needs to be applied. The new `veeam_vbr_set_postgres_database_server_limits` module hosted in this collection can assist in this regard.

### Veeam Backup & Replication Console

- Install/Upgrade only available for versions 12.1 and later

### Veeam ONE

- Install/Patch/Upgrade only supports Windows authentication (no SQL authentication)
  - _This is a limitation of the Ansible Role and not the Veeam Product._

## Example Playbooks

Please note there are more configurations than the examples shown below. If you have any questions, please feel free to create an [issue](https://github.com/VeeamHub/veeam-ansible/issues/new/choose).

### Veeam Backup & Replication Community Edition Install with ISO Download (v12.1+)

```yaml
- name: Veeam Backup & Replication Install
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: vbr_install
      vars:
        version: "12"
        iso_download: true
```

### Veeam Backup & Replication Community Edition Install with ISO Download (v12)

```yaml
- name: Veeam Backup & Replication Install
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: vbr_install
      vars:
        version: "12"
        iso_download: true
        sql_install_username: "sql_install"
        sql_install_password: "ChangeM3!"
        sql_service_username: "svc_sql"
        sql_service_password: "ChangeM3!"
        sql_username: "postgres"
        sql_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable
```

### Veeam Backup & Replication Community Edition Install with ISO Download (v11-)

```yaml
- name: Veeam Backup & Replication Install
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: vbr_install
      vars:
        version: "11"
        iso_download: true
        sql_install_username: "sql_install"
        sql_install_password: "ChangeM3!"
        sql_service_username: "svc_sql"
        sql_service_password: "ChangeM3!"
        sql_username: "sa"
        sql_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable
```

### Veeam Backup & Replication Install with ISO Download (v12.1+)

```yaml
- name: Veeam Backup & Replication Install
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: vbr_install
      vars:
        version: "12"
        iso_download: true
        license: true
        source_license: "/root/ansible/license.lic"
```

### Veeam Backup & Replication Install with ISO Download (v12-)

```yaml
- name: Veeam Backup & Replication Install
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: vbr_install
      vars:
        version: "12"
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

### Veeam Backup & Replication Install with ISO Download and remote Microsoft SQL (v12.1+)

```yaml
- name: Veeam Backup & Replication Install with Remote Microsoft SQL Server
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: vbr_install
      vars:
        version: "12"
        license: true
        source_license: "/root/ansible/license.lic"
        sql_express_setup: false
        sql_engine: "0" # 0-MSSQL / 1-Postgres (default)
        sql_authentication: "1" # 0-Windows (default) 1-Native
        sql_instance: "sql.contoso.local"
        sql_username: "svc_veeam"
        sql_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable
```

### Veeam Backup & Replication Install with ISO Download and remote PostgreSQL (v12.1+)

```yaml
- name: Veeam Backup & Replication Install with Remote PostgreSQL Server
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: vbr_install
      vars:
        version: "12"
        license: true
        source_license: "/root/ansible/license.lic"
        sql_express_setup: false
        sql_authentication: "1" # 0-Windows (default) 1-Native
        sql_instance: "sql.contoso.local"
        sql_username: "svc_veeam"
        sql_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable
    - name: Applying tuning on a remote PostgreSQL server running as the VBR DB
       veeamhub.veeam.veeam_vbr_set_postgres_database_server_limits:
         os_type: Windows
         cpu_count: 16
         ram_gb: 30
```

### Veeam Backup & Replication Install with ISO Download and remote Microsoft SQL (v12)

```yaml
- name: Veeam Backup & Replication Install with Remote Microsoft SQL Server
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: vbr_install
      vars:
        version: "12"
        license: true
        source_license: "/root/ansible/license.lic"
        sql_express_setup: false
        sql_engine: "0" # 0-MSSQL / 1-Postgres (default)
        sql_instance: "sql.contoso.local"
        sql_username: "svc_veeam"
        sql_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable
```

### Veeam Backup & Replication Install with ISO Download and remote PostgreSQL (v12)

```yaml
- name: Veeam Backup & Replication Install with Remote PostgreSQL Server
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: vbr_install
      vars:
        version: "12"
        license: true
        source_license: "/root/ansible/license.lic"
        sql_express_setup: false
        sql_instance: "sql.contoso.local"
        sql_username: "svc_veeam"
        sql_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable
    - name: Applying tuning on a remote PostgreSQL server running as the VBR DB
       veeamhub.veeam.veeam_vbr_set_postgres_database_server_limits:
         os_type: Windows
         cpu_count: 16
         ram_gb: 30
```

### Veeam Backup & Replication Install with ISO Download and remote SQL (v11-)

```yaml
- name: Veeam Backup & Replication Install with Remote SQL Server
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: vbr_install
      vars:
        version: "11"
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
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: vbr_install
      vars:
        version: "12"
        destination: "C:\\install\\"
        destination_iso_file: "VeeamBackup&Replication_12.0.0.1420_20230209.iso"
        sql_install_username: "sql_install"
        sql_install_password: "ChangeM3!"
        sql_service_username: "svc_sql"
        sql_service_password: "ChangeM3!"
        sql_username: "sa"
        sql_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable
```

### Veeam Backup & Replication Upgrade - Native Auth (v12.1+)

```yaml
- name: Veeam Backup & Replication Upgrade
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: vbr_upgrade
      vars:
        version: "12"
        iso_download: true
        license: true
        source_license: "/root/ansible/license.lic"
        sql_authentication: "1" # 0-Windows (default) 1-Native
        sql_password: "ChangeM3!"
```

### Veeam Backup & Replication Upgrade - Windows Auth (v12.1+)

```yaml
- name: Veeam Backup & Replication Upgrade
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: vbr_upgrade
      vars:
        version: "12"
        iso_download: true
        license: true
        source_license: "/root/ansible/license.lic"
```

### Veeam Backup & Replication Upgrade (v12-)

```yaml
- name: Veeam Backup & Replication Upgrade
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: vbr_upgrade
      vars:
        version: "12"
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
        version: "12"
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
        patch_file: "VeeamBackup&Replication_10.0.0.4461.update0.exe"
```

### Veeam Backup Enterprise Manager Install without ISO Download (v12.1+)

```yaml
- name: Veeam Backup Enterprise Manager Install
  gather_facts: false
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: em_install
      vars:
        version: "12"
        destination: "C:\\install\\"
        destination_iso_file: "VeeamBackup&Replication_12.0.0.1420_20230209.iso"
        license: true #mandatory for EM
        source_license: "/root/ansible/license.lic"
```

### Veeam Backup Enterprise Manager Install without ISO Download (v12-)

```yaml
- name: Veeam Backup Enterprise Manager Install
  gather_facts: false
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: em_install
      vars:
        version: "12"
        destination: "C:\\install\\"
        destination_iso_file: "VeeamBackup&Replication_12.0.0.1420_20230209.iso"
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

### Veeam Backup Enterprise Manager Install with ISO Download and remote Microsoft SQL (v12.1+)

```yaml
- name: Veeam Backup Enterprise Manager Install
  gather_facts: false
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: em_install
      vars:
        version: "12"
        iso_download: true
        license: true #mandatory for EM
        source_license: "/root/ansible/license.lic"
        sql_express_setup: false
        sql_engine: "0" # 0-MSSQL / 1-Postgres (default)
        sql_authentication: "1" # 0-Windows (default) 1-Native
        sql_instance: "sql.contoso.local"
        sql_username: "svc_veeam"
        sql_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable
```

### Veeam Backup Enterprise Manager Install with ISO Download and remote PostgreSQL (v12.1+)

```yaml
- name: Veeam Backup Enterprise Manager Install
  gather_facts: false
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: em_install
      vars:
        version: "12"
        iso_download: true
        license: true #mandatory for EM
        source_license: "/root/ansible/license.lic"
        sql_express_setup: false
        sql_authentication: "1" # 0-Windows (default) 1-Native
        sql_instance: "sql.contoso.local"
        sql_username: "svc_veeam"
        sql_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable
```

### Veeam Backup Enterprise Manager Install with ISO Download and remote Microsoft SQL (v12)

```yaml
- name: Veeam Backup Enterprise Manager Install
  gather_facts: false
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: em_install
      vars:
        version: "12"
        iso_download: true
        license: true #mandatory for EM
        source_license: "/root/ansible/license.lic"
        sql_express_setup: false
        sql_engine: "0" # 0-MSSQL / 1-Postgres (default)
        sql_instance: "sql.contoso.local"
        sql_username: "svc_veeam"
        sql_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable
```

### Veeam Backup Enterprise Manager Install with ISO Download and remote PostgreSQL (v12)

```yaml
- name: Veeam Backup Enterprise Manager Install
  gather_facts: false
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: em_install
      vars:
        version: "12"
        iso_download: true
        license: true #mandatory for EM
        source_license: "/root/ansible/license.lic"
        sql_express_setup: false
        sql_instance: "sql.contoso.local"
        sql_username: "svc_veeam"
        sql_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable
```

### Veeam Backup Enterprise Manager Install with ISO Download and remote SQL (v11-)

```yaml
- name: Veeam Backup Enterprise Manager Install
  gather_facts: false
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: em_install
      vars:
        version: "11"
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
  gather_facts: false
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: em_install
      vars:
        version: "12"
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

### Veeam Backup Enterprise Manager Upgrade - Native Auth (v12.1+)

```yaml
- name: Backup Enterprise Manager Upgrade
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: em_upgrade
      vars:
        version: "12"
        iso_download: true
        license: true
        source_license: "/root/ansible/license.lic"
        sql_authentication: "1" # 0-Windows (default) 1-Native
        sql_password: "ChangeM3!"
```

### Veeam Backup Enterprise Manager Upgrade - Windows Auth (v12.1+)

```yaml
- name: Backup Enterprise Manager Upgrade
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: em_upgrade
      vars:
        version: "12"
        iso_download: true
        license: true
        source_license: "/root/ansible/license.lic"
```

### Veeam Backup Enterprise Manager Upgrade (v12-)

```yaml
- name: Backup Enterprise Manager Upgrade
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: em_upgrade
      vars:
        version: "12"
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
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
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

### Veeam Backup & Replication Console Install

```yaml
- name: Veeam Backup & Replication Console Install
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: vbr_console_install
      vars:
        version: "12"
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
        version: "12"
        destination: "C:\\install\\"
        destination_iso_file: "VeeamBackup&Replication_12.1.1.56_20240127.iso"
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
        version: "12"
        iso_download: true
```

### Veeam ONE Install - Typical Deployment (single server)

```yaml
- name: Installing Veeam ONE Install (Typical Deployment)
  gather_facts: false
  hosts: veeam

  vars:
    version: "12"
    iso_download: false #this way ISO is only downloaded once
    license: true
    source_license: "/root/ansible/license.lic"
    sql_express_setup: true
    sql_service_username: "svc_sql"
    sql_service_password: "ChangeM3!"
    one_create_service_account: true #true==local false==domain
    one_username: "svc_one"
    one_password: "ChangeM3!"
    # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable
  tasks:
    - name: Veeam ONE Server installation tasks
      include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: one_server_install
      vars:
        iso_download: true #this way ISO is only downloaded once
    - name: Veeam ONE Web UI installation tasks
      include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: one_web_ui_install
    - name: Veeam ONE Monitoring Client installation tasks
      include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: one_client_install
```

### Veeam ONE Community Edition Install - Typical Deployment (single server)

```yaml
- name: Installing Veeam ONE Install (Typical Deployment)
  gather_facts: false
  hosts: veeam

  vars:
    version: "12"
    iso_download: false #this way ISO is only downloaded once
    sql_express_setup: true
    sql_service_username: "svc_sql"
    sql_service_password: "ChangeM3!"
    one_create_service_account: true #true==local false==domain
    one_username: "svc_one"
    one_password: "ChangeM3!"
    # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable
  tasks:
    - name: Veeam ONE Server installation tasks
      include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: one_server_install
      vars:
        iso_download: true #this way ISO is only downloaded once
    - name: Veeam ONE Web UI installation tasks
      include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: one_web_ui_install
    - name: Veeam ONE Monitoring Client installation tasks
      include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: one_client_install
```

### Veeam ONE Install - Advanced Deployment (multi-server)

```yaml
- name: Veeam ONE Advanced Deployment - Veeam ONE Server
  gather_facts: false
  hosts: server
  tasks:
    - name: Veeam ONE Server installation tasks
      include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: one_server_install
      vars:
        version: "12"
        iso_download: true
        license: true
        source_license: "/root/ansible/license.lic"
        sql_express_setup: false
        sql_instance: "sql.contoso.local"
        sql_database: "VeeamOne"
        one_installation_type: "1" #1-Advanced | 2-Backup data only | 3-Typical
        one_create_service_account: false #true==local false==domain
        one_username: "contoso\\jsmith"
        one_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable

- name: Veeam ONE Advanced Deployment - Veeam Web UI
  gather_facts: false
  hosts: web
  tasks:
    - name: Veeam ONE Web UI installation tasks
      include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: one_web_ui_install
      vars:
        version: "12"
        iso_download: true
        one_create_service_account: false #true==local false==domain
        one_username: "contoso\\jsmith"
        one_password: "ChangeM3!"
        one_server: "server.contoso.local"
        # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable

- name: Veeam ONE Advanced Deployment - Monitoring Client
  gather_facts: false
  hosts: client
  tasks:
    - name: Veeam ONE Monitoring Client installation tasks
      include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: one_client_install
      vars:
        version: "12"
        iso_download: true
        one_server: "server.contoso.local"
```

### Veeam ONE Install - Typical Deployment and remote SQL

```yaml
- name: Installing Veeam ONE Install (Typical Deployment)
  gather_facts: false
  hosts: veeam

  vars:
    version: "12"
    iso_download: false #this way ISO is only downloaded once
    license: true
    source_license: "/root/ansible/license.lic"
    sql_express_setup: false
    sql_instance: "sql.contoso.local"
    sql_database: "VeeamOne"
    one_create_service_account: false #true==local false==domain
    one_username: "contoso\\jsmith"
    one_password: "ChangeM3!"
    # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable
  tasks:
    - name: Veeam ONE Server installation tasks
      include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: one_server_install
      vars:
        iso_download: true #this way ISO is only downloaded once
    - name: Veeam ONE Web UI installation tasks
      include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: one_web_ui_install
    - name: Veeam ONE Monitoring Client installation tasks
      include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: one_client_install
```

### Veeam ONE Typical Upgrade

```yaml
- name: Veeam ONE Upgrade
  gather_facts: false
  hosts: veeam

  vars:
    version: "12"
    iso_download: false  #this way ISO is only downloaded once
    license: true
    source_license: "/root/ansible/license.lic"
    one_username: "svc_one"
    one_password: "ChangeM3!"
    # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable
  tasks:
    - name: Veeam ONE Server upgrade tasks
      include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: one_server_upgrade
      vars:
        iso_download: true  #this way ISO is only downloaded once
    - name: Veeam ONE Web UI upgrade tasks
      include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: one_web_ui_upgrade
    - name: Veeam ONE Monitoring Client upgrade tasks
      include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: one_client_upgrade
    - name: Rebooting server now to complete upgrade
      ansible.windows.win_reboot:
        msg: Reboot initiated by Ansible to complete Veeam ONE upgrade
```

### Veeam ONE Upgrade - Advanced Deployment (multi-server)

```yaml
- name: Veeam ONE Advanced Deployment - Veeam ONE Server
  gather_facts: false
  hosts: server
  tasks:
    - name: Veeam ONE Server upgrade tasks
      include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: one_server_upgrade
      vars:
        version: "12"
        iso_download: true
        license: true
        source_license: "/root/ansible/license.lic"
        sql_instance: "sql.contoso.local"
        sql_database: "VeeamOne"
        one_username: "contoso\\jsmith"
        one_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable

- name: Veeam ONE Advanced Deployment - Veeam Web UI
  hosts: web
  gather_facts: false
  tasks:
    - name: Veeam ONE Web UI upgrade tasks
      include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: one_web_ui_upgrade
      vars:
        version: "12"
        iso_download: true
        one_username: "contoso\\jsmith"
        one_password: "ChangeM3!"
        one_server: "server.contoso.local"
        # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable

- name: Veeam ONE Advanced Deployment - Monitoring Client
  hosts: client
  gather_facts: false
  tasks:
    - name: Veeam ONE Monitoring Client upgrade tasks
      include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: one_client_upgrade
      vars:
        version: "12"
        iso_download: true
        one_server: "server.contoso.local"
```

### Veeam ONE Patch

```yaml
- name: Veeam ONE Patch
  hosts: veeam
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vas
        tasks_from: one_patch
      vars:
        source: "C:\\install\\"
        patch_file: "VeeamONE_9.5.4.4587_Update#4a.exe"
        one_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/user_guide/playbooks_vault.html#single-encrypted-variable
```
