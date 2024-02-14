==============================
veeamhub.veeam Release Notes
==============================

.. contents:: Topics

This changelog describes changes after version 1.5.0.

v2.1.0
======

Breaking Changes
-------------

- Changed default ISO checksum algorithm from SHA256 to SHA1 (https://github.com/VeeamHub/veeam-ansible/issues/46)

Minor Changes
-------------

- Added support for version 12.1
- Updated ISO to version 12.1 (https://github.com/VeeamHub/veeam-ansible/issues/59)
- Updated logic for ISO download (https://github.com/VeeamHub/veeam-ansible/issues/57)
- Added support for specifying install directory for 12.1 and later (https://github.com/VeeamHub/veeam-ansible/issues/51)
- Added support for installing VBR plugins for 12.1 and later (https://github.com/VeeamHub/veeam-ansible/issues/25)
- Updated ansible-lint - Now using latest ansible-lint 6.22.2 (https://github.com/VeeamHub/veeam-ansible/issues/33)
- Updated collection dependencies - Validated this collection supports the most current version of dependencies (ansible.windows/community.windows)

Bugfixes
--------

- Fixed lint errors - Made necessary changes to conform with current best practices
- Added retry when starting Veeam services (https://github.com/VeeamHub/veeam-ansible/issues/54)
