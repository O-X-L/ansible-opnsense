#!/usr/bin/env bash

set -e

cd "$(dirname "$0")/.."

echo ''
echo 'BUILDING tarball'
echo ''

rm -f oxlorg-opnsense-*.tar.gz
ansible-galaxy collection build

echo "CHECK CONTENT: 'tar --list -f oxlorg-opnsense-*.tar.gz'"
