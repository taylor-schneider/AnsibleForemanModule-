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
import os
import sys
import logging
from ansible.module_utils.basic import AnsibleModule
from ForemanApiWrapper.ForemanApiUtilities.ForemanApiWrapper import ForemanApiWrapper
from ForemanApiWrapper.ApiStateEnforcer.ApiStateEnforcer import ApiStateEnforcer



PY3 = sys.version_info >= (3, 0)

# Configure logging format and level
logFormat = '%(asctime)s,%(msecs)d %(levelname)-8s [%(module)s:%(funcName)s():%(lineno)d] %(message)s'

logging.basicConfig(format=logFormat,
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Configure the logging framework to log to console
#logger.addHandler(logging.StreamHandler(sys.stdout))

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
            state=dict(type='str', required=False),
            log_path=dict(type='str', required=False)
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
        api_url = module.params["apiUrl"]
        username = module.params["username"]
        password = module.params["password"]
        verify_ssl = module.params["verifySsl"]
        record = module.params["record"]
        desired_state = module.params["state"]
        log_path = module.params['log_path']

        # Setup the log directory
        try:
            if log_path is not None:
                if not os.path.exists(log_path):
                    log_dir = os.path.dirname(log_path)
                    if not os.path.isdir(log_dir):
                        os.makedirs(log_dir, exist_ok=True)

                # Configure the logger
                fh = logging.FileHandler(log_path)
                fh.setLevel(logging.DEBUG)
                logger.addHandler(fh)
        except Exception as e:
            # logging is best effort
            module.warn("An error occurred while configuring log file:")
            module.warn(e.args[0])

        # Ensure the desired state exists
        foreman_api_wrapper = ForemanApiWrapper(username, password, api_url, verify_ssl)
        api_state_enforcer = ApiStateEnforcer(foreman_api_wrapper)
        modification_receipt = api_state_enforcer.ensure_state(desired_state, record)

        result.update(modification_receipt.__dict__)

        # In the event of a successful module execution, you will want to
        # simple AnsibleModule.exit_json(), passing the key/value results
        module.exit_json(**result)

    except Exception as e:
        # Log the exception
        logging.exception(e)

        # Cause the task to fail
        error_msg = 'The module failed to run.'
        result["exception"] = e
        if module:
            module.fail_json(msg=error_msg, **result)
        else:
            raise Exception(error_msg) from e

def main():
    run_module()

if __name__ == '__main__':
    main()
