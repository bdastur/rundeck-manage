#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml
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
        jobs = []

        for project in projects:
            joblist = self.rdclient.list_jobs(project['name'])
            for job in joblist:
                jobs.append(job)

        return jobs

    def backup_rundeck(self, localdir, fmt='yaml'):
        '''
        The API is invoked to backup Rundeck projects and
        job definitions.
        :type localdir: String
        :param localdir: Local Directory to save the job definitions.
        '''
        if not os.path.isdir(localdir):
            print "Require a valid directory to save job descriptions"
            return None

        jobs = self.list_all_jobs()
        for job in jobs:
            # First create a directory for the project.
            proj_dir = os.path.join(localdir, job['project'])
            if not os.path.exists(proj_dir):
                os.mkdir(proj_dir)

            retcode = self.rdclient.export_job(job['id'], fmt=fmt)
            jobfile = job['id'] + ".yaml"
            jobfile = os.path.join(proj_dir, jobfile)
            with open(jobfile, 'w') as outfile:
                outfile.write(retcode.text)




