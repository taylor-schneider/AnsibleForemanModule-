#!/bin/bash

set -e

pip3 install requests

bash Tests/AnsibleModuleTester/InstallDependencies.sh
bash ForemanApiWrapper/InstallDependencies.sh