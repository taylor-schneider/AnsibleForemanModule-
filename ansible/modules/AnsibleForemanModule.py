#!/usr/bin/python

# Copyright: (c) 2018, Taylor Schneider <tschneider@live.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# This is a simple example module I wrote
# Its purpose is to give a simple idea of the internals of an ansibalz module
# We can see the parameters this module takes and the results it will return
# In the test module we will see how this module can be tested


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''

'''

EXAMPLES = '''

'''

RETURN = '''

'''

import logging

import os
for line in os.environ['PYTHONPATH'].split(os.pathsep):
    print(line)

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.foobar.foo import foo

logger = logging.getLogger()

def run_module():
    module = None
    try:

        # Seed the results dict incase anything happens
        result = {"changed": False}

        # Define available arguments/parameters a user can pass to the module
        # See: https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html
        module_args = dict(
            apiUrl=dict(type='str', required=True),
            username=dict(type='str', required=True),
            password=dict(type='str', required=True),
            verifySsl=dict(type='bool', required=True),
            record=dict(type='dict', required=True),
            action=dict(type='str', required=True),
            state=dict(type='str', required=False)
        )

#        recordType, desiredState, record = ModuleArgumentParser.ParseModuleArguments(stdinJsonString)

        # Once we have parsed the arguments we can continue on
#        module_args[recordType] = dict(type='dict', required=True)

        # The AnsibleModule object will be our abstraction working with Ansible
        # this includes instantiation, a couple of common attr would be the
        # args/params passed to the execution, as well as if the module
        # supports check mode
        module = AnsibleModule(
            argument_spec=module_args,
            supports_check_mode=True
        )

        # If the user is working with this module in only check mode we do not
        # want to make any changes to the environment, just return the current
        # state with no modifications
        if module.check_mode:
            raise Exception("Check mode is not yet supported.")

        # Now that the module has been created, extract the params
        apiUrl = module.params["apiUrl"]
        username = module.params["username"]
        password = module.params["password"]
        verifySsl = module.params["verifySsl"]


        # Ensure the desired state exists
#        apiWrapper = ForemanApiWrapper(username, password, apiUrl, verifySsl)
#        stateEnforcer = ApiStateEnforcer(apiWrapper)
#        result = stateEnforcer.EnsureState(recordType, desiredState, record)
        result = {}
        result["foo"] = foo.foo()

        # In the event of a successful module execution, you will want to
        # simple AnsibleModule.exit_json(), passing the key/value results
        module.exit_json(**result)

    except Exception as e:
        errorMsg = 'The module failed to run.'
        result["exception"] = e
        if module:
            module.fail_json(msg=errorMsg, **result)
        else:
            raise Exception(errorMsg) from e

def main():
    run_module()

if __name__ == '__main__':
    main()