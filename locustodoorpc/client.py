# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html)

import json
import os
import sys
import time

import odoorpc
from locust import Locust, events

PY3 = sys.version[0] == 3

if PY3:
    import urllib
    from urllib import parse as urlparse
else:
    import urllib2 as urllib
    from urlparse import urlparse


class ODOOLocustClient(odoorpc.ODOO):

    def capture_request(request_type):
        def _wrapped_func(func):
            def _wrapper(self, *args, **kwargs):
                if (args[0] == '/jsonrpc' and
                        args[1].get('method').startswith('execute')):
                    # example of name: /jsonrpc | product.product: search
                    name = "%s | %s: %s" % tuple(
                        [args[0]] + args[1]['args'][3:5]
                    )
                else:
                    name = args[0]
                start_time = time.time()
                try:
                    response = func(self, *args, **kwargs)
                except (urllib.HTTPError, urllib.URLError) as err:
                    total_time = int((time.time() - start_time) * 1000)
                    events.request_failure.fire(
                        request_type=request_type,
                        name=name,
                        response_time=total_time,
                        exception=err
                    )
                    raise
                else:
                    total_time = int((time.time() - start_time) * 1000)
                    if isinstance(response, dict):  # jsonrpc
                        size = len(json.dumps(response))
                    else:  # http
                        response = response.read()
                        size = len(response)
                    events.request_success.fire(
                        request_type=request_type,
                        name=name,
                        response_time=total_time,
                        response_length=size
                    )
                    return response
            return _wrapper
        return _wrapped_func

    @capture_request('jsonrpc')
    def json(self, url, params):
        return super(ODOOLocustClient, self).json(url, params)

    @capture_request('http')
    def http(self, url, data=None, headers=None):
        return super(ODOOLocustClient, self).http(url, data=data,
                                                  headers=headers)


class OdooRPCLocust(Locust):
    """ Locust class providing the odoorpc client

    This is the abstract Locust class which should be subclassed. It provides
    an Odoo client using odoorpc library, that can be used to make requests
    that will be tracked in Locust's statistics.

    The host, port and protocol (jsonrpc or jsonrpc+ssl) comes from the
    ``--host`` option.

    """

    db_name = os.getenv('ODOO_DB_NAME', 'odoo')
    login = os.getenv('ODOO_LOGIN', 'admin')
    password = os.getenv('ODOO_PASSWORD', 'admin')

    # allow to force Odoo version (avoid auto-detection)
    version = os.getenv('ODOO_VERSION')

    def __init__(self, *args, **kwargs):
        super(OdooRPCLocust, self).__init__(*args, **kwargs)
        url = urlparse(self.host)
        port = url.port
        if url.scheme == 'https':
            protocol = 'jsonrpc+ssl'
            if not port:
                port = 443
        else:
            protocol = 'jsonrpc'
            if not port:
                port = 80
        protocol = 'jsonrpc+ssl' if url.scheme == 'https' else 'jsonrpc'
        params = {
            'host': url.hostname,
            'port': port,
            'protocol': protocol,
        }
        if self.version:
            params['version'] = self.version
        self.client = ODOOLocustClient(**params)
