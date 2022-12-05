Locust odoorpc
==============

Links
-----

* Locust: https://locust.io/
* Locust docs: https://docs.locust.io/
* OdooRPC: https://pythonhosted.org/OdooRPC/
* Source code: https://github.com/camptocamp/locustodoorpc
* Alternative: https://github.com/nseinlet/OdooLocust (using ``openerplib`` instead of ``odoorpc``)

Description
-----------

Locust custom client integrating the `odoorpc <https://github.com/osiell/odoorpc>`_ library, so you can run load-testing on your odoo services. Have a look at the feature list of `locust <https://github.com/locustio/locust/#description>`_ to see what you can do.

Installation
------------

::

  virtualenv .env
  source .env/bin/activate
  pip install locustodoorpc

Usage
-----

For the general documentation on Locust, heads on https://docs.locust.io/en/latest/
A few options can be customized with environment variables or command line parameters. These
can also be specified in the Locust Web UI now.

+--------------+------------------+-------------------------------------------------------------+
|Name          |Option            |Usage                                                        |
+--------------+------------------+-------------------------------------------------------------+
|ODOO_DB_NAME  |--odoo-db-name    |Configure the name of the database to load-test              |
|              |                  |(default: odoo)                                              |
+--------------+------------------+-------------------------------------------------------------+
|ODOO_LOGIN    |--odoo-login      |Login to use for the actions (default: admin)                |
+--------------+------------------+-------------------------------------------------------------+
|ODOO_PASSWORD |--odoo-password   |Password for the user (default: admin)                       |
+--------------+------------------+-------------------------------------------------------------+
|ODOO_VERSION  |--odoo-version    |Force an Odoo version (e.g. 9.0, 10.0, 11.0), normally       |
|              |                  |automatically recognized                                     |
+--------------+------------------+-------------------------------------------------------------+

Example::

  ODOO_DB_NAME=demo locust -f examples/locustfile.py --host http://localhost:8069 


Also Valid::

  locust -f examples/locustfile.py --host http://localhost:8069 --odoo-db-name=demo


Check the `examples <https://github.com/camptocamp/locustodoorpc/tree/master/examples>`_

.. image:: https://raw.githubusercontent.com/camptocamp/locustodoorpc/master/images/locustodoorpc.png

