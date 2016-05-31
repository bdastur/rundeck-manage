#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from rundeck.client import Rundeck


class RundeckClient(object):
    def __init__(self,
                 rundeck_url,
                 apitoken):
        self.rundeck_url = rundeck_url
        self.apitoken = apitoken

        self.rdclient = Rundeck(self.rundeck_url,
                                api_token=self.apitoken,
                                headers={'Accept': 'application/json'})

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

        :type fmt: String
        :param fmt: Format of the job description

        Note: The directory structure created under the localdir is
                <localdir>/<project name>/<job_id>.yaml
        '''
        if not os.path.isdir(localdir):
            print "Require a valid directory to save job descriptions"
            return

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

    def populate_rundeck(self, localdir, fmt='yaml'):
        '''
        The API is invoked to populate Rundeck with projects and
        jobs from a local repository.

        :type localdir: String
        :param localdir: Local repository to read the job files.

        :type fmt: String
        :param fmt: Format of the job description file

        NOTE: The directory structure expected is:
            <localdir>/<project name>/<job_id>.yaml
        '''
        if not os.path.isdir(localdir):
            print "Required a valid directory to read job definitions"
            return None

        #for osobj in os.walk(localdir):
        #    print "osobj: %s, %s, %s " % (osobj[0], osobj[1], osobj[2])

        projects = []
        for dirobj in os.listdir(localdir):
            dirpath = os.path.join(localdir, dirobj)
            if os.path.isdir(dirpath):
                projects.append(dirobj)


        currprojects = self.rdclient.list_projects()
        currprojlist = []
        for proj in currprojects:
            currprojlist.append(proj['name'])

        for project in projects:
            # First check if the project exists.
            # If it does skip it.
            print "project: ", project
            if project in currprojlist:
                print "No need to create project %s" % project
            else:
                print "create project ", project
                projectconfig = {}
                projectconfig['description'] = "%s: (Automation created)" % \
                    project
                retval = self.rdclient.create_project(project,
                                                      config=projectconfig)
                print "Project create: ", retval

        # Now import job files
        for project in projects:
            dirpath = os.path.join(localdir, dirobj)
            if not os.path.isdir(dirpath):
                print "Not a directory %s, skip it" % dirpath
                continue

            for filename in os.listdir(dirpath):
                jobfile = os.path.join(dirpath, filename)
                print "JOb file: ", jobfile
                retval = self.rdclient.import_job_file(jobfile,
                                                       project=project,
                                                       file_format=fmt)
                print "retval: ", retval





