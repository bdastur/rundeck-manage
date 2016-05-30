#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import api.rdeck_client as rdeckclient


class ClientUt(unittest.TestCase):
    def SetUp(self):
        print "Setupp"

    def test_basic(self):
        rdeck_url = os.environ.get('_RDECK_URL', None)
        apikey = os.environ.get('_RDECK_APIKEY', None)

        self.failUnless(rdeck_url is not None)
        self.failUnless(apikey is not None)

        rdclient = rdeckclient.RundeckClient(rdeck_url, apikey)
        self.failUnless(rdclient.rdclient is not None)

        rdclient.list_all_jobs()
