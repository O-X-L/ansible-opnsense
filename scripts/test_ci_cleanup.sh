#!/usr/bin/env bash

set -eo pipefail

echo ''

DEBUG=false
TMP_DIR="/tmp/.opnsense_test_$(date +%s)"
TMP_COL_DIR="${TMP_DIR}/collections"

export ANSIBLE_INVENTORY_UNPARSED_WARNING=False
export ANSIBLE_LOCALHOST_WARNING=False
export ANSIBLE_NO_TARGET_SYSLOG=True

cd "$(dirname "$0")/.."
LOCAL_COLLECTION="$(pwd)"
VERBOSITY=''
export SUCCEEDED=''
export FAILED=''
EXIT_CODE=0

set -u

source 'scripts/test_prep.sh'  # shared between single/multi test

function run_test_soft() {
  module="$1"
  check_mode="$2"
  run_test "$module" "$check_mode"
  if [[ "$?" == '0' ]]
  then
    if [[ -n "$SUCCEEDED" ]]
    then
      export SUCCEEDED="${SUCCEEDED}, "
    fi
    export SUCCEEDED="${SUCCEEDED}${module}"
  else
    if [[ -n "$FAILED" ]]
    then
      export FAILED="${FAILED}, "
    fi
    export FAILED="${FAILED}${module}"
    EXIT_CODE=1
  fi
}

cd "$TMP_COL_DIR/ansible_collections/oxlorg/opnsense"

echo ''
echo '##############################'
echo '           CLEANUP'
echo '##############################'
echo ''

set +e
run_test_soft '1_cleanup' 0

rm -rf "$TMP_DIR"

exit "$EXIT_CODE"
