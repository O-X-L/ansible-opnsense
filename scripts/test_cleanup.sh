#!/usr/bin/env bash

set -e

echo ''

TMP_DIR="/tmp/.opnsense_test_$(date +%s)"
TMP_COL_DIR="$TMP_DIR/collections"

export ANSIBLE_NO_TARGET_SYSLOG=True

if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]
then
  echo 'Arguments:'
  echo '  1: firewall'
  echo '  2: api key file'
  echo "  3: path to local collection - set to '0' to clone from github"
  echo '  4: path to virtual environment (optional)'
  echo ''
  exit 1
else
  export TEST_FIREWALL="$1"
  export TEST_API_CREDS_FILE="$2"
fi

LOCAL_COLLECTION="$3"

if [ -n "$4" ]
then
  source "$4/bin/activate"
fi

set -u

source "$(dirname "$0")/test_prep.sh"  # shared

cd "$TMP_COL_DIR/ansible_collections/oxlorg/opnsense"

echo ''
echo 'RUNNING CLEANUP'
echo ''

ansible-playbook tests/1_cleanup.yml

echo ''
echo 'FINISHED CLEANUP!'
echo ''

rm -rf "$TMP_DIR"
