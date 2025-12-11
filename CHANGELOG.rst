==============================
veeamhub.veeam Release Notes
==============================

.. contents:: Topics

This changelog describes changes after version 1.5.0.

v2.3.4
======

Major Changes
-------------

- Added support for v13

Minor Changes
-------------

- Updated ISO references to latest versions (https://github.com/VeeamHub/veeam-ansible/issues/75)
- Added logic to enable/disable Cloud Connect maintenance mode before/after Veeam Backup & Replication upgrade
- Added support to adjust time to wait for long running tasks to complete (https://github.com/VeeamHub/veeam-ansible/issues/73)

Bugfixes
-------------

- Added logic to disable/enable backup jobs before/after Veeam Backup & Replication upgrade (https://github.com/VeeamHub/veeam-ansible/issues/74)
- Added logic to ensure Veeam services are started before proceeding with upgrade (https://github.com/VeeamHub/veeam-ansible/issues/27)


Breaking Changes
-------------

- Deprecated support for installing Veeam Backup & Replication version 11 and earlier.
- Deprecated support for installing Veeam ONE. Depending on demand, Veeam ONE support may be reintroduced in a future release.

v2.2.5
======

Minor Changes
-------------

- Added options to configuration additional Veeam Backup & Replication jobs settings (https://github.com/VeeamHub/veeam-ansible/pull/79)

v2.2.4
======

Bugfixes
--------

- Fixed being unable to deploy VBR using LocalSystem account on a local PostgreSQL instance (https://github.com/VeeamHub/veeam-ansible/issues/80)

v2.2.3
======

Minor Changes
-------------

- Updated ISO to version 12.1.2.172 20240515 (https://github.com/VeeamHub/veeam-ansible/issues/64)

Bugfixes
--------

- Added playbook validation for unsupported SQL server settings (https://github.com/VeeamHub/veeam-ansible/issues/68)
- Updated Veeam ONE sample playbooks (https://github.com/VeeamHub/veeam-ansible/issues/69)


v2.2.2
======

Bugfixes
--------

- Fixed incorrect ISO specified for Veeam ONE v12 (https://github.com/VeeamHub/veeam-ansible/issues/65)
- Fixed SQL Express installation account not being created (https://github.com/VeeamHub/veeam-ansible/issues/66)


v2.2.1
======

Breaking Changes
-------------

- Changed default ISO checksum algorithm from SHA256 to SHA1 (https://github.com/VeeamHub/veeam-ansible/issues/46)

Major Changes
-------------

- Added support for new silent install process available in version 12.1 (https://helpcenter.veeam.com/docs/backup/vsphere/install_vbr_answer_file.html?ver=120)
- Added support for new silent install process available in version 12.1 (https://helpcenter.veeam.com/docs/backup/vsphere/upgrade_vbr_answer_file.html?ver=120)
- Added support for Veeam Backup & Replication Console 12.1 install (https://helpcenter.veeam.com/docs/backup/vsphere/install_console_answer_file.html?ver=120)
- Added support for Veeam Backup & Replication Console 12.1 upgrade (https://helpcenter.veeam.com/docs/backup/vsphere/upgrade_console_answer_file.html?ver=120)

Minor Changes
-------------

- Updated ISO to version 12.1 (https://github.com/VeeamHub/veeam-ansible/issues/59)
- Updated logic for ISO download (https://github.com/VeeamHub/veeam-ansible/issues/57)
- Added support for specifying install directory for 12.1 and later (https://github.com/VeeamHub/veeam-ansible/issues/51)
- Added support for installing VBR plugins for 12.1 and later (https://github.com/VeeamHub/veeam-ansible/issues/25)
- Updated ansible-lint - Now using ansible-lint 6.22.2 (https://github.com/VeeamHub/veeam-ansible/issues/33)
- Updated collection dependencies - Validated this collection supports the most current version of dependencies (ansible.windows/community.windows)

Bugfixes
--------

- Fixed lint errors - Made necessary changes to conform with current best practices
- Added retry when starting Veeam services (https://github.com/VeeamHub/veeam-ansible/issues/54)

Deprecations
--------

- Dropping support for installing version 10
