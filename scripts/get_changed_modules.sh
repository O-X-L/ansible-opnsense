#!/usr/bin/env bash

if [ -z "$1" ]
then
  echo "ERROR: Requires file containing list of changed files as argument 1"
  exit 1
fi
if [ -z "$2" ]
then
  echo "ERROR: Requires output-file as argument 2"
  exit 1
fi

CHANGES_FILE="$1"
OUT_FILE="$2"

set -euo pipefail

i=0
while IFS= read -r file
do
  i=$(( i + 1))
  echo "$i $file"
done < "$CHANGES_FILE"
