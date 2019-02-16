#!/bin/bash

set -e

# Determine location
CURRENT_FILE=$(realpath ${BASH_SOURCE[0]})
CURRENT_DIRECTORY=$(dirname $CURRENT_FILE)

pip3 install requests

bash "$CURRENT_DIRECTORY/Tests/AnsibleModuleTester/InstallDependencies.sh"
bash "$CURRENT_DIRECTORY/ansible/module_utils/ForemanApiWrapper/InstallDependencies.sh"
