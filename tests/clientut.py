#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import api.rdeck_client as rdeckclient


class ClientUt(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.rdeck_url = None
        self.apikey = None
        self.rdclient = None
        super(ClientUt, self).__init__(*args, **kwargs)

    def setUp(self):
        self.rdeck_url = os.environ.get('_RDECK_URL', None)
        self.apikey = os.environ.get('_RDECK_APIKEY', None)

        if self.rdeck_url is None or self.apikey is None:
            print "_RDECK_URL and _RDECK_APIKEY ENV variables required"

        self.rdclient = rdeckclient.RundeckClient(self.rdeck_url,
                                                  self.apikey)

    def test_basic(self):

        self.failUnless(self.rdeck_url is not None)
        self.failUnless(self.apikey is not None)
        self.failUnless(self.rdclient.rdclient is not None)

        jobs = self.rdclient.list_all_jobs()
        for job in jobs:
            print "JOB: ", job

    def test_backup_rundeck(self):
        print "Test Rundeck Backup"
        self.failUnless(self.rdeck_url is not None)
        self.failUnless(self.apikey is not None)

        self.rdclient.backup_rundeck("/tmp/testdir")

