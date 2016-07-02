#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import api.rdeck_client as rdeckclient
import rundeck.exceptions
from rundeck.client import Rundeck


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

    def test_populate_rundeck(self):
        print "Test Rundeck Populate"
        self.failUnless(self.rdeck_url is not None)
        self.failUnless(self.apikey is not None)
        self.failUnless(self.rdclient.rdclient is not None)

        self.rdclient.populate_rundeck("/tmp/testdir")

    def test_rundeckrun_project_create(self):
        print "Test basic project create API"
        self.failUnless(self.rdeck_url is not None)
        self.failUnless(self.apikey is not None)
        self.failUnless(self.rdclient.rdclient is not None)

        projectconfig = {}
        projectconfig['description'] = "Test project (API creation)"

        try:
            retval = self.rdclient.rdclient.create_project('testproject202',
                                                           config=projectconfig)
        except rundeck.exceptions.HTTPError as httperror:
            print "Error: %s" % httperror
            return

        print "Retval: ", retval

    def test_rundeckrun_project_get(self):
        print "Test basic get project API"
        self.failUnless(self.rdeck_url is not None)
        self.failUnless(self.apikey is not None)
        self.failUnless(self.rdclient.rdclient is not None)

        # Valid project.
        #retval = self.rdclient.rdclient.get_project('testproj3')
        #print "retval: ", retval

        kwargs = {}

        kwargs['headers'] = {'Accept': 'application/json'}
        # Invalid project.
        self.rdclient.rdclient.get_project('dummy', **kwargs)

    def test_list_executions(self):
        print "Test listing executions from Rundeck API"
        rdclient = Rundeck(self.rdeck_url,
                           api_token=self.apikey,
                           headers={'Accept': 'application/json'})
        projects = rdclient.list_projects()
        for project in projects:
            print "project: ", project

        jobs = rdclient.list_jobs(project="testproj3")
        for job in jobs:
            job_id = job['id']
            print "JOb id: ", job_id
            executions = rdclient.list_job_executions(job_id,
                                                      max=20,
                                                      offset=0)
            for execution in executions:
                print "Execution: ", execution










