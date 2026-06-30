#!/usr/bin/env bash

set -eo pipefail

echo ''

DEBUG=false
TMP_DIR="/tmp/.opnsense_test_$(date +%s)"
TMP_COL_DIR="${TMP_DIR}/collections"
FILE_MODULES_TO_TEST='/tmp/changed_modules.txt'

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
echo '        STARTING TESTS!'
echo '##############################'
echo ''

set +e
run_test_soft '1_dependencies' 0

count="$(cat "$FILE_MODULES_TO_TEST" | wc -l)"
i=0
while read m
do
  i=$(( i + 1))
  echo "########## TEST ${i}/${count} ##########"
  run_test_soft "$m" 1
done < "$FILE_MODULES_TO_TEST"

echo ''
echo '##############################'
echo '        FINISHED TESTS!'
echo '##############################'
echo ''

echo ''
echo '##############################'
echo '           CLEANUP'
echo '##############################'
echo ''

run_test_soft '1_cleanup' 0

echo '##############################'
echo '           RESULTS:'
if echo "$USER" | grep -q 'test'
then
  echo "SUCCEEDED: ${SUCCEEDED}"
  echo "FAILED: ${FAILED}"
else
  printf "\033[0;32mSUCCEEDED: ${SUCCEEDED}\033[0m\n"
  printf "\033[0;31mFAILED: ${FAILED}\033[0m\n"
fi

echo '##############################'

rm -rf "$TMP_DIR"

exit "$EXIT_CODE"
