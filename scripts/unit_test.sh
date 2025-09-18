#!/usr/bin/env bash

set -e

cd "$(dirname "$0")/.."

mkdir -p /tmp/ansible_pytest/collections/ansible_collections/ansibleguy
rm -f /tmp/ansible_pytest/collections/ansible_collections/ansibleguy/opnsense
ln -s $(pwd) /tmp/ansible_pytest/collections/ansible_collections/ansibleguy/opnsense

pytest --cov
