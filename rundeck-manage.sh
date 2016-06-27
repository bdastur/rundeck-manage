#!/bin/bash

#######################################################
# Rundeck Manage script.
#
#######################################################

directory=
rundeck_url=
rundeck_apikey=

function show_help()
{
    echo "`basename $0`: Rundeck Manage"
    echo "---------------------------------"
    echo ""
    echo "-d directory    : Specify the destination directory where the rundeck job data will be saved"
    echo ""
    echo "-u rundeck url  : Rundeck URL"
    echo ""
    echo "-h              : Show this help"
    echo ""
    echo "Example Usage: "
    echo "export _RDECK_APIKEY=AKF449EKFJELEJ"
    echo "export _RDECK_USER=testuser"
    echo "export _RDECK_SSHKEY=/tmp/tf_accesskey"
    echo " ./rundeck-manage.sh backup -u test.rundeck.abc.com -d /tmp/testdir"
    echo ""

    exit 1
}

function backup_rundeck()
{
    rundeck_url=$1
    localdir=$2
    rundeck_apikey=$3

    if [[ ! -e $localdir ]]; then
        echo "Local directory does not exist"
        exit 1
    fi

    jobsdir="${localdir}/jobs"
    if [[ ! -d $jobsdir ]]; then
        echo "Jobs Directory does not exist. Create it"
        mkdir -p $jobsdir
    fi

    python - << END
import api.rdeck_client as rdeckclient

rdclient = rdeckclient.RundeckClient("${rundeck_url}",
                                     "${rundeck_apikey}")
rdclient.backup_rundeck("${jobsdir}")
END
    # Backup Data directory.
    scp -r -i ${_RDECK_SSHKEY} ${_RDECK_USER}@${rundeck_url}:/var/lib/rundeck/data $localdir

    # Backup logs.
    scp -r -i ${_RDECK_SSHKEY} ${_RDECK_USER}@${rundeck_url}:/var/lib/rundeck/logs $localdir

}

readonly COMMANDLINE="$*"

if [[ $# -eq 0 ]]; then
    echo "Error: No options provided"
    echo ""
    show_help
fi

operation_type=$1
if [[ ! $operation_type = "backup" ]]; then
    echo "Operation type invalid"
    exit 1
fi
shift

CMD_OPTIONS="d:u:h"

while getopts ${CMD_OPTIONS} option; do
    case $option in
        d)
            directory=$OPTARG
            ;;
        u)
            rundeck_url=$OPTARG
            ;;
        h)
            show_help
            ;;
        :) echo "Error: Option -${OPTARG} needs arguments";;
        *) echo "Error: Invalid Option \"-${OPTARG}\"";;
    esac
done

# Validate input.
if [[ -z $directory ]]; then
    echo "Need to specify a local directory to save rundeck info"
    exit 1
fi

if [[ -z ${_RDECK_APIKEY} ]]; then
    echo "Set env variable _RDECK_APIKEY to the API TOken for Rundeck"
    exit 1
fi

if [[ -z ${_RDECK_SSHKEY} ]]; then
    echo "Set env variable _RDECK_SSHKEY to the ssh private key to access Rundeck server"
    exit 1
fi

if [[ -z ${_RDECK_USER} ]]; then
    echo "Set env var _RDECK_USER to the ssh user to access Rundeck Server"
    exit 1
fi

if [[ $operation_type = "backup" ]]; then
    backup_rundeck $rundeck_url $directory ${_RDECK_APIKEY}
fi






 echo "export _RDECK_APIKEY=AKF449EKFJELEJ"
     echo "export _RDECK_USER=testuser"
         echo "export _RDECK_SSHKEY=/tmp/tf_accesskey"
