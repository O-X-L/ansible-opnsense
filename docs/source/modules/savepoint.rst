.. _modules_savepoint:

.. include:: ../_include/head.rst

==================
Firewall Savepoint
==================

**STATE**: removed

Contribution
************

Thanks to `@Rath <https://github.com/superstes>`_ for developing this module!

----

Info
****

.. warning::

    OPNsense 26.7 removed the firewall savepoint API (`opnsense/core#10411 <https://github.com/opnsense/core/pull/10411>`_).

    The :code:`savepoint`, :code:`revert` and :code:`cancelRollback` endpoints of the :code:`filter`, :code:`source_nat`, :code:`one_to_one` and :code:`d_nat` controllers no longer exist and :code:`apply` no longer accepts a rollback revision.

    There is no replacement. This module always fails and should be removed from your playbooks.
