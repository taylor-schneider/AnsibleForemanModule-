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

from ansible.module_utils.basic import AnsibleModule
from ForemanApiUtilities.ForemanApiWrapper import ForemanApiWrapper
from ApiStateEnforcer.ApiStateEnforcer import ApiStateEnforcer

def run_module():
    module = None
    try:

        module_args = dict(
            apiUrl=dict(type='str', required=True),
            username=dict(type='str', required=True),
            password=dict(type='str', required=True),
            verifySsl=dict(type='bool', required=True),
            record=dict(type='dict', required=True),
            action=dict(type='str', required=True),
            state=dict(type='str', required=False)
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

        # The record should contain the record type
        recordType = ApiStateEnforcer._get_record_type_from_record(record)

        # Ensure the desired state exists
        foremanApiWrapper = ForemanApiWrapper(username, password, apiUrl, verifySsl)
        apiStateEnforcer = ApiStateEnforcer(foremanApiWrapper)
        result = apiStateEnforcer.EnsureState(recordType, desiredState, record)

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
