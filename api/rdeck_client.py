#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rundeck.client import Rundeck


class RundeckClient(object):
    def __init__(self,
                 rundeck_url,
                 apitoken):
        self.rundeck_url = rundeck_url
        self.apitoken = apitoken

        self.rdclient = Rundeck(self.rundeck_url,
                                api_token=self.apitoken)

    def list_all_jobs(self):
        '''
        List all the jobs from all projects and return
        a json object
        '''
        projects = self.rdclient.list_projects()
        print "Projects: ", projects

        for project in projects:
            joblist = self.rdclient.list_jobs(project['name'])
            print "Jobs: ", joblist

