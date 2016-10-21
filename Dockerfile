FROM centos:7
MAINTAINER behzad_dastur@symantec.com

RUN yum install -y \
    git 

RUN mkdir /workspace
RUN mkdir /workspace/api

RUN git clone http://github.com/bdastur/rundeckrun.git  /workspace/rundeckrun
RUN git clone http://github.com/ansible/ansible.git -b stable-1.9  /workspace/ansible_stable
RUN cd /workspace/ansible_stable && git submodule update --init --recursive

ADD ./rundeck-manage.sh  /workspace/rundeck-manage.sh
ADD ./api/* /workspace/api/


CMD [/bin/bash]

