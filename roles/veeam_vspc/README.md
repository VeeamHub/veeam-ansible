# veeamhub.veeam.veeam_vspc

An Ansible Role to install [Veeam Service Provider Console](https://www.veeam.com/service-provider-console.html) (VSPC).

- [veeamhub.veeam.veeam\_vspc](#veeamhubveeamveeam_vspc)
  - [How to use this Role](#how-to-use-this-role)
  - [Requirements](#requirements)
    - [Ansible](#ansible)
    - [OS](#os)
    - [Veeam Software](#veeam-software)
  - [Available Task Files](#available-task-files)
  - [Role Variables](#role-variables)
    - [Common Variables](#common-variables)
    - [Server Component Variables](#server-component-variables)
    - [Additional Server Component Variables](#additional-server-component-variables)
    - [Web UI Component Variables](#web-ui-component-variables)
    - [ConnectWise Manage Plugin Variables](#connectwise-manage-plugin-variables)
    - [File-Level Restore Plugin Variables](#file-level-restore-plugin-variables)
  - [Known Issues](#known-issues)
  - [Example Playbooks](#example-playbooks)
    - [VSPC Server Install with Remote SQL Server (Windows Authentication)](#vspc-server-install-with-remote-sql-server-windows-authentication)
    - [VSPC Server Install with Remote SQL Server (SQL Authentication)](#vspc-server-install-with-remote-sql-server-sql-authentication)
    - [VSPC Web UI Install (co-located with Server)](#vspc-web-ui-install-co-located-with-server)
    - [VSPC Web UI Install (remote Server)](#vspc-web-ui-install-remote-server)
    - [VSPC Server Install with Advanced ConnectWise Manage Plugin Configuration](#vspc-server-install-with-advanced-connectwise-manage-plugin-configuration)
    - [VSPC Server Install with Advanced File-Level Restore Plugin Configuration](#vspc-server-install-with-advanced-file-level-restore-plugin-configuration)
    - [VSPC Web UI Install with Advanced File-Level Restore UI Component Configuration](#vspc-web-ui-install-with-advanced-file-level-restore-ui-component-configuration)
    - [VSPC Server Install without Plugins](#vspc-server-install-without-plugins)
    - [VSPC Web UI Install without Plugins](#vspc-web-ui-install-without-plugins)

## How to use this Role

This role is part of a [collection](https://galaxy.ansible.com/veeamhub/veeam) of all roles in this repository. The easiest method to install it is using [Ansible Galaxy](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html):

```bash
ansible-galaxy collection install veeamhub.veeam
```

## Requirements

Requirements listed are not complete and only include configurations tested during development and use of this Ansible Role. Keep in mind these requirements are in addition to Veeam's system requirements for the software to be installed/upgraded. For more information, please reference the [Veeam Service Provider Console Deployment Guide](https://helpcenter.veeam.com/docs/vac/deployment/overview.html?ver=9.2).

This collection depends on Windows modules (`ansible.windows` & `community.windows`) that are not standard in Ansible anymore (2.10.x). If the collection is installed using the Ansible Galaxy CLI (see previous section), no further action is required on your part.

### Ansible

- Ansible 2.16+

### OS

- Microsoft Windows Server 2025
- Microsoft Windows Server 2022
- Microsoft Windows Server 2019

> **Important:** This role does **not** support installing VSPC using SQL Express. A pre-existing Microsoft SQL Server instance (local or remote) must be available before running this role. SQL Express provisioning is not performed by any task in this role.

### Veeam Software

- Veeam Service Provider Console
  - v9

## Available Task Files

This role does **not** run any tasks from `tasks/main.yml` by default. All functionality is invoked via `tasks_from` in `include_role`. The following task files are available:

| Task File | Description |
|---|---|
| `vspc_server_install` | Installs the VSPC Server component and optionally the ConnectWise Manage and/or File-Level Restore plugin server components. |
| `vspc_ui_install` | Installs the VSPC Web UI component and optionally the ConnectWise Manage and/or File-Level Restore plugin Web UI components. |

> **Note:** Upgrade task files (`vspc_server_upgrade`, `vspc_ui_upgrade`) are not yet implemented in this role. Upgrade support is planned for a future release.

## Role Variables

Variables are located in two different locations:

- Default: _defaults/main.yml_
- Software-specific: _vars/_

### Common Variables

| Variable | Default | Description |
|---|---|---|
| `version` | `"9"` | Major version of VSPC to install. Only `"9"` is currently supported. |
| `veeam_retries` | `60` | Number of retries for long-running operations (ISO download, install). Each retry is 60 seconds; 60 retries = max 1 hour. |
| `skip_iso_check` | `false` | Skip the ISO version verification check. |
| `iso_download` | `false` | Download the ISO from the internet. Set to `true` to download automatically. |
| `iso_checksum_algorithm` | `"sha1"` | Checksum algorithm used when verifying the downloaded ISO. |
| `source_license` | `""` | Path on the Ansible controller to the VSPC license file. **Required** for install. |
| `destination` | `"C:\\install\\"` | Working directory on the target Windows server for ISO and log files. |

### Server Component Variables

| Variable | Default | Description |
|---|---|---|
| `sql_instance` | `"(local)\\VEEAMSQL2017"` | SQL Server instance to use for the VSPC database. |
| `sql_database` | `"VSPC"` | Name of the VSPC SQL database. |
| `sql_authentication` | `"0"` | SQL authentication mode. `0` = Windows Authentication, `1` = SQL Server Authentication. |
| `sql_username` | `""` | SQL user name. Required when `sql_authentication: "1"`. Use Ansible Vault for sensitive values. |
| `sql_password` | `""` | SQL user password. **Required** when `sql_authentication: "1"`. Use Ansible Vault for sensitive values. |
| `vspc_server_management_port` | `"1989"` | Port for Web UI to Server communication. Used by both `vspc_server_install` and `vspc_ui_install`. |
| `vspc_connection_hub_port` | `"9999"` | Port for cloud agent and VCC connections to the VSPC Server. Also used by the FLR Web UI component. |
| `create_service_account` | `false` | Create a local Windows user account to run the VSPC service. |
| `service_account_username` | `""` | Windows account under which VSPC services run. Must not be `LocalSystem`. **Required** — the installer will fail if left empty. Use Ansible Vault for sensitive values. |
| `service_account_password` | `""` | Password for the service account. **Required** — the installer will fail if left empty. Use Ansible Vault. |

### Additional Server Component Variables

| Variable | Default | Description |
|---|---|---|
| `vspc_license_autoupdate` | `"1"` | Enable automatic license update and usage reporting. Required for NFR and Evaluation licenses. `1` = enabled (default). |
| `vspc_product_updates` | `"1"` | Enable automatic update check for managed Veeam products. `1` = enabled (default). |
| `vspc_server_certificate_thumbprint` | _(not set)_ | Thumbprint of an existing certificate to use for the VSPC server TLS endpoint. If not set, the installer generates a self-signed certificate. Example: `"C4CCFEE30EFBD201749DEE3D0DBFCA50155342CD"`. |

### Web UI Component Variables

| Variable | Default | Description |
|---|---|---|
| `vspc_server_name` | `"localhost"` | FQDN or IP address of the VSPC Server. Used when installing the Web UI on a separate host. |
| `vspc_website_port` | `"1280"` | Port for browser access to the VSPC Web UI. |
| `vspc_configure_schannel` | `"1"` | Enable high security mode (TLS 1.2, disables weak ciphers). `1` = enabled (default). |
| `vspc_server_account_name` | `"{{ service_account_username }}"` | Windows account the Web UI service uses to authenticate to the VSPC Server. Defaults to `service_account_username`. Must not be `LocalSystem`. **Required** — the installer will fail if left empty. Use Ansible Vault for sensitive values. |
| `vspc_server_account_password` | `"{{ service_account_password }}"` | Password for `vspc_server_account_name`. Defaults to `service_account_password`. **Required** — the installer will fail if left empty. Use Ansible Vault. |

### ConnectWise Manage Plugin Variables

The `vspc_connectwise_plugin` flag controls installation of both the server component (via `vspc_server_install`) and the Web UI component (via `vspc_ui_install`).

| Variable | Default | Description |
|---|---|---|
| `vspc_connectwise_plugin` | `true` | Set to `false` to skip installation of the ConnectWise Manage Plugin components. |
| `vspc_cwm_server_name` | `"{{ vspc_server_name }}"` | FQDN or IP of the VSPC Server the CWM plugin server component connects to. |
| `vspc_cwm_communication_port` | `"9996"` | Port the CWM plugin uses to communicate with VSPC. |
| `vspc_cwm_username` | `"{{ service_account_username }}"` | Account under which the CWM plugin service runs (must have local Admin). Defaults to `service_account_username`. Use Ansible Vault. |
| `vspc_cwm_password` | `"{{ service_account_password }}"` | Password for `vspc_cwm_username`. Defaults to `service_account_password`. Use Ansible Vault. |
| `vspc_cwm_server_account_name` | `"{{ service_account_username }}"` | Account used by the CWM plugin to connect to the VSPC server (must have local Admin). Defaults to `service_account_username`. |
| `vspc_cwm_server_account_password` | `"{{ service_account_password }}"` | Password for `vspc_cwm_server_account_name`. Defaults to `service_account_password`. Use Ansible Vault. |

### File-Level Restore Plugin Variables

The `vspc_flr_restore_plugin` flag controls installation of both the server component (via `vspc_server_install`) and the Web UI component (via `vspc_ui_install`).

| Variable | Default | Description |
|---|---|---|
| `vspc_flr_restore_plugin` | `true` | Set to `false` to skip installation of the File-Level Restore Plugin components. |
| `vspc_flr_hub_host_name` | `"{{ vspc_server_name }}"` | FQDN or IP of the VSPC Web UI server. Used by the FLR Web UI component to connect to VSPC. |
| `vspc_flr_service_account_name` | `"{{ service_account_username }}"` | Account under which the FLR server service runs (must have local Admin). Defaults to `service_account_username`. |
| `vspc_flr_service_account_password` | `"{{ service_account_password }}"` | Password for `vspc_flr_service_account_name`. Defaults to `service_account_password`. Use Ansible Vault. |
| `vspc_flr_hub_account_name` | `"{{ service_account_username }}"` | Account used by the FLR Web UI component to connect to VSPC (must have local Admin). Defaults to `service_account_username`. |
| `vspc_flr_hub_account_password` | `"{{ service_account_password }}"` | Password for `vspc_flr_hub_account_name`. Defaults to `service_account_password`. Use Ansible Vault. |

## Known Issues

- **SQL Express is not supported.** This role does not install or configure SQL Express. A pre-existing Microsoft SQL Server instance (local or remote) must be present before running `vspc_server_install`. VSPC v9 supports Microsoft SQL Server only — PostgreSQL is not supported.
- **Upgrade tasks are not yet implemented.** The task files `vspc_server_upgrade` and `vspc_ui_upgrade` do not currently exist in this role. If VSPC is already installed, the install tasks (`vspc_server_install`, `vspc_ui_install`) will halt with an error directing you to use the upgrade task. Upgrade support is planned for a future release.
- The `iso_checksum` variable in `vars/vspc_v9.yml` should be verified against the downloaded ISO before use. It is strongly recommended to confirm the checksum from the [Veeam download page](https://www.veeam.com/downloads.html).
- Sensitive values such as `sql_password`, `service_account_password`, `vspc_server_account_password`, `vspc_cwm_password`, `vspc_flr_service_account_password`, and `vspc_flr_hub_account_password` should be encrypted using [Ansible Vault](https://docs.ansible.com/ansible/latest/vault_guide/vault_encrypting_content.html#creating-encrypted-variables).
- The VSPC Server and Web UI can be installed on the same host or on separate hosts. When installing on separate hosts, set `vspc_server_name` to the FQDN or IP of the VSPC Server host before running `vspc_ui_install`.
- The `vspc_connectwise_plugin` and `vspc_flr_restore_plugin` flags apply to both the server and Web UI install task files. Run `vspc_server_install` first (server components), then `vspc_ui_install` (Web UI components) using the same flag values.

## Example Playbooks

Please note there are more configurations than the examples shown below. If you have any questions, please feel free to create an [issue](https://github.com/VeeamHub/veeam-ansible/issues/new/choose).

### VSPC Server Install with Remote SQL Server (Windows Authentication)

```yaml
- name: Veeam Service Provider Console Server Install with Remote SQL Server
  hosts: vspc
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vspc
        tasks_from: vspc_server_install
      vars:
        version: "9"
        iso_download: true
        source_license: "/root/ansible/vspc-license.lic"
        sql_authentication: "0"
        sql_instance: "sql.contoso.local"
        service_account_username: "svc_vspc"
        service_account_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/vault_guide/vault_encrypting_content.html#creating-encrypted-variables
```

### VSPC Server Install with Remote SQL Server (SQL Authentication)

```yaml
- name: Veeam Service Provider Console Server Install with Remote SQL Server
  hosts: vspc
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vspc
        tasks_from: vspc_server_install
      vars:
        version: "9"
        iso_download: true
        source_license: "/root/ansible/vspc-license.lic"
        sql_authentication: "1"
        sql_instance: "sql.contoso.local"
        sql_username: "svc_vspc"
        sql_password: "ChangeM3!"
        service_account_username: "svc_vspc"
        service_account_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/vault_guide/vault_encrypting_content.html#creating-encrypted-variables
```

### VSPC Web UI Install (co-located with Server)

```yaml
- name: Veeam Service Provider Console Web UI Install
  hosts: vspc
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vspc
        tasks_from: vspc_ui_install
      vars:
        version: "9"
        iso_download: true
        service_account_username: "svc_vspc"
        service_account_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/vault_guide/vault_encrypting_content.html#creating-encrypted-variables
```

### VSPC Web UI Install (remote Server)

```yaml
- name: Veeam Service Provider Console Web UI Install
  hosts: vspc_webui
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vspc
        tasks_from: vspc_ui_install
      vars:
        version: "9"
        iso_download: true
        vspc_server_name: "vspc-server.contoso.local"
        service_account_username: "svc_vspc"
        service_account_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/vault_guide/vault_encrypting_content.html#creating-encrypted-variables
```

### VSPC Server Install with Advanced ConnectWise Manage Plugin Configuration

```yaml
- name: Veeam Service Provider Console Server Install with ConnectWise Manage Plugin
  hosts: vspc
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vspc
        tasks_from: vspc_server_install
      vars:
        version: "9"
        iso_download: true
        source_license: "/root/ansible/vspc-license.lic"
        service_account_username: "svc_vspc"
        service_account_password: "ChangeM3!"
        vspc_cwm_server_name: "vspc.contoso.local"
        vspc_cwm_username: "CONTOSO\\cwm.svc"
        vspc_cwm_password: "ChangeM3!"
        vspc_cwm_server_account_name: "Administrator"
        vspc_cwm_server_account_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/vault_guide/vault_encrypting_content.html#creating-encrypted-variables
```

### VSPC Server Install with Advanced File-Level Restore Plugin Configuration

```yaml
- name: Veeam Service Provider Console Server Install with File-Level Restore Plugin
  hosts: vspc
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vspc
        tasks_from: vspc_server_install
      vars:
        version: "9"
        iso_download: true
        source_license: "/root/ansible/vspc-license.lic"
        service_account_username: "svc_vspc"
        service_account_password: "ChangeM3!"
        vspc_flr_service_account_name: "CONTOSO\\flr.svc"
        vspc_flr_service_account_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/vault_guide/vault_encrypting_content.html#creating-encrypted-variables
```

### VSPC Web UI Install with Advanced File-Level Restore UI Component Configuration

```yaml
- name: Veeam Service Provider Console Web UI Install with File-Level Restore UI Component
  hosts: vspc_webui
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vspc
        tasks_from: vspc_ui_install
      vars:
        version: "9"
        iso_download: true
        vspc_server_name: "vspc-server.contoso.local"
        service_account_username: "svc_vspc"
        service_account_password: "ChangeM3!"
        vspc_flr_hub_host_name: "vspc-webui.contoso.local"
        vspc_flr_hub_account_name: "Administrator"
        vspc_flr_hub_account_password: "ChangeM3!"
        # https://docs.ansible.com/ansible/latest/vault_guide/vault_encrypting_content.html#creating-encrypted-variables
```

### VSPC Server Install without Plugins

```yaml
- name: Veeam Service Provider Console Server Install without Plugins
  hosts: vspc
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vspc
        tasks_from: vspc_server_install
      vars:
        version: "9"
        iso_download: true
        source_license: "/root/ansible/vspc-license.lic"
        service_account_username: "svc_vspc"
        service_account_password: "ChangeM3!"
        vspc_connectwise_plugin: false
        vspc_flr_restore_plugin: false
        # https://docs.ansible.com/ansible/latest/vault_guide/vault_encrypting_content.html#creating-encrypted-variables
```

### VSPC Web UI Install without Plugins

```yaml
- name: Veeam Service Provider Console Web UI Install without Plugins
  hosts: vspc
  tasks:
    - include_role:
        name: veeamhub.veeam.veeam_vspc
        tasks_from: vspc_ui_install
      vars:
        version: "9"
        iso_download: true
        service_account_username: "svc_vspc"
        service_account_password: "ChangeM3!"
        vspc_connectwise_plugin: false
        vspc_flr_restore_plugin: false
        # https://docs.ansible.com/ansible/latest/vault_guide/vault_encrypting_content.html#creating-encrypted-variables
```
