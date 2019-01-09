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

from ansible.module_utils.basic import AnsibleModule

def run_module():
    try:
        # Define available arguments/parameters a user can pass to the module
        # See: https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html
        module_args = dict(
            apiUrl=dict(type='str', required=True),
            username=dict(type='str', required=True),
            password=dict(type='str', required=True),
            verifySsl=dict(type='bool', required=True),
            desiredState=dict(type='dict', required=False),
            apiEndpoint = dict(type='str', required=True),
            httpMethod = dict(type='str', required=True),
        )

        # seed the result dict in the object
        # we primarily care about changed and state
        # change is if this module effectively modified the target
        # state will include any data that you want your module to pass back
        # for consumption, for example, in a subsequent task
        result = dict(
            changed=False
        )

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
            return result

        # Now that the module has been created, extract the params
        apiUrl = module.params["apiUrl"]
        username = module.params["username"]
        password = module.params["password"]
        verifySsl = module.params["verifySsl"]
        desiredState = module.params["desiredState"]
        apiEndpoint = module.params["apiEndpoint"]
        httpMethod = module.params["httpMethod"]

        # Ensure the desired state exists
        pass

        # Use whatever logic you need to determine whether or not this module
        # made any modifications to your target
        #
        # In this example we will just assume it was changed
        if True:
            result['changed'] = True

        # In the event of a successful module execution, you will want to
        # simple AnsibleModule.exit_json(), passing the key/value results
        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg='The module failed to run.', **result)

def main():
    run_module()

if __name__ == '__main__':
    main()