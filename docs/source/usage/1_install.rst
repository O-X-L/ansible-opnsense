.. _usage_install:

.. include:: ../_include/head.rst

================
1 - Installation
================


Ansible
*******

See `the documentation <https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#pip-install>`_ on how to install Ansible.

If you DO NOT want to use Ansible - `this fork <https://github.com/O-X-L/opnsense-api-client>`_ provides you with a raw Python3 interface.

Dependencies
************

The `httpx python-module <https://www.python-httpx.org/>`_ or `requests python-module <https://requests.readthedocs.io/>`_ is used for API communications!

.. code-block:: bash

    python3 -m pip install --upgrade httpx
    # or
    python3 -m pip install --upgrade requests


Note: If both are installed, "httpx" is preferred by default. You can set the preferred http-client-library using the environmental-variable `HTTP_CLIENT` to a value of "httpx" or "requests".

Collection
**********

.. code-block:: bash

    # stable version:
    ansible-galaxy collection install oxlorg.opnsense

    # latest version:
    ansible-galaxy collection install git+https://github.com/O-X-L/ansible-opnsense.git

    # install to specific directory for easier development
    cd $PLAYBOOK_DIR
    ansible-galaxy collection install git+https://github.com/O-X-L/ansible-opnsense.git -p ./collections
