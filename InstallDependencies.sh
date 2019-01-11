#!/bin/bash

set -e

pip3 install requests

bash AnsibleForemanModule/Tests/AnsibleModuleTester/InstallDependencies.sh
bash ForemanApiWrapper/InstallDependencies.sh
