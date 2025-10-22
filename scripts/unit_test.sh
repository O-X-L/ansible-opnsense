#!/usr/bin/env bash

set -e

cd "$(dirname "$0")/.."

mkdir -p /tmp/ansible_pytest/collections/ansible_collections/oxlorg
rm -f /tmp/ansible_pytest/collections/ansible_collections/oxlorg/opnsense
ln -s $(pwd) /tmp/ansible_pytest/collections/ansible_collections/oxlorg/opnsense

pytest --cov $@
