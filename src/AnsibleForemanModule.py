#!/usr/bin/python

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
import sys
import json
from ansible.module_utils.basic import AnsibleModule
from ForemanApiWrapper.ForemanApiUtilities.ForemanApiWrapper import ForemanApiWrapper
from ForemanApiWrapper.ApiStateEnforcer.ApiStateEnforcer import ApiStateEnforcer
from ForemanApiWrapper.RecordUtilities import ForemanApiRecord

PY3 = sys.version_info >= (3, 0)


def run_module():
    module = None
    result = {}
    try:
        module_args = dict(
            apiUrl=dict(type='str', required=True),
            username=dict(type='str', required=True),
            password=dict(type='str', required=True),
            verifySsl=dict(type='bool', required=True),
            record=dict(type='dict', required=True),
            state=dict(type='str', required=False)
        )

        module = AnsibleModule(
            argument_spec=module_args,
            supports_check_mode=False
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
        desiredState = module.params["state"]
        record = module.params["record"]

        # Ensure the desired state exists
        foremanApiWrapper = ForemanApiWrapper(username, password, apiUrl, verifySsl)
        apiStateEnforcer = ApiStateEnforcer(foremanApiWrapper)
        modification_receipt = apiStateEnforcer.ensure_state(desiredState, record)

        result.update(modification_receipt.__dict__)

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
