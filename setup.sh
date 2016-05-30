#!/bin/bash

##################################################
# A setup script to setup the environment.
##################################################

# Git Repos.
rundeckrun_repo="https://github.com/bdastur/rundeckrun.git"
rundeckrun_branch="master"
rundeckrun_localdir="../rundeckrun"

ansible_repo="http://github.com/ansible/ansible.git"
ansible_branch="stable-1.9"
ansible_localdir="../ansible_stable19"


curdir=`pwd`
rootdir=${curdir%/*}

ansible_path="${rootdir}/ansible_stable19"
ansible_submodules_repo="${ansible_path}/lib/ansible/modules/core/.git"

rundeckrun_path="${rootdir}/rundeckrun"
pythonpath="${rundeckrun_path}"

echo $curdir
echo $rootdir
echo $ansible_path
echo $rundeckrun_path

# The function pulls a git repository
# :params
#   $1: reponame
#   $2: localdir
#   $3: branch
# It skips pulling the repo if the local dir
# already exists.
function git_pull () 
{
    gitrepo=$1
    localgitrepo=$2
    branch=$3

    if [[ ! -z $branch ]]; then
        branch="-b $branch"
    fi

    echo -n "pulling repo: [$gitrepo]  "
    if [[ ! -d $localgitrepo ]]; then 
        echo "Pulling $gitrepo $branch" 
        git clone $gitrepo $branch $localgitrepo 
    fi

    if [[ -d $localgitrepo ]]; then
        echo " ---> [DONE]"
    else
        echo " ---> [FAILED]";echo
        echo "Error logs: $setup_logs"
    fi
}

git_pull ${rundeckrun_repo} ${rundeckrun_localdir} ${rundeckrun_branch}
git_pull ${ansible_repo} ${ansible_localdir} ${ansible_branch}

# Add Ansible submodules
if [[ ! -e ${ansible_submodules_repo} ]]; then
    cd ${ansible_path}
    git submodule update --init --recursive
    cd ${curdir}
fi

# Environment Setup.
export ANSIBLE_HOST_KEY_CHECKING=False

export PYTHONPATH=${pythonpath}
#######################################
# Source ansible environment.
#######################################
source ../ansible_stable19/hacking/env-setup


