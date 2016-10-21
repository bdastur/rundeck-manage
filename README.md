# rundeck-manage
----

Manage Rundeck: Users, Projects, Jobs.

Rundeck is an open source software, that helps automate operational tasks. To see the full details of what Rundeck can do refer to the [Rundeck Users guide](http://rundeck.org/docs/manual/introduction.html).

This repository has tools to automate managing Rundeck. Like creating users and managing ACL Policies. Managing projects and Jobs.

Set the Following Environment variables:
---
_RDECK_SSHKEY=<path to access key>
_RDECK_USER=<rundeck user>
_RDECK_URL=<run deck url>
_RDECK_APIKEY=<api key>

NOTE:
When specifying the _RDECK_URL, do not include http:// or https://

---

Populate Rundeck:

Example of populating rundeck with project and job definitions from local repository:

./rundeck-manage.sh populate -u rundeckserver.abc.net -d /home/behzad_dastur/rdeckjun21prod/aws_rundeck/rundeck-backup/jobs/

Backup Rundeck:

Example of taking a backup of job definitiosn, projects, logs and DB from rundeck to local repository

./rundeck-manage.sh backup -u rundeck.abc.net -d /home/behzad_dastur/rdeckjun21prod/aws_rundeck/rundeck-backup/ -s

# Taking a backup from prod server.
source ~/rundeck_exports_100_122_2_41 
./rundeck-manage.sh backup -u 100.122.2.41 -d /home/behzad_dastur/awsrundeck_aug1/aws_rundeck/rundeck-oct21/

