==============================
veeamhub.veeam Release Notes
==============================

.. contents:: Topics

This changelog describes changes after version 1.5.0.

v1.8.0
======

Breaking Changes
-------------

- Changed ISO checksum algorithm from SHA256 to SHA1 (https://github.com/VeeamHub/veeam-ansible/issues/46)

Minor Changes
-------------

- Updated ansible-lint - Now using latest ansible-lint 6.22.2 (https://github.com/VeeamHub/veeam-ansible/issues/33)
- Updated collection dependencies - Validated this collection supports the most current version of dependencies (ansible.windows/community.windows)

Bugfixes
--------

- Fixed lint errors - Made necessary changes to conform with current best practices
- Added retry when starting Veeam services (https://github.com/VeeamHub/veeam-ansible/issues/54)
