# Ansible Foreman Module
This repository contains an ansible module which wraps around the ForemanApiWrapper library. It allows users to manage Foreman using ansible.

## OS Package Dependencies
Outside the python dependencies there are OS dependencies that need to be installed

### The PyYAML package
This package will install the python package named yaml

This package can be installed on CentOS/RHEL will the following command:

`yum -y install PyYAML`

### The ansible package
There is a python package called ansible. There is also an OS package names ansible. 

While the OS package is not explicitly required it is reccommended to install it as it makes the behavior more consistent.

For example it will place a config file at `/etc/ansible/ansible.cfg`

This package can be installed on CentOS/RHEL will the following command:

`yum -y install ansible`

## Testing Modules

### Debugging Modules
In order for Modules to be debugged through the IDE, the `src/` directory will need to be added to the `PYTHONPATH` variable.

In PyCharm, this can be marking the `src/` directory as a "Sources Root".

For more information see the AnsibleModuleTester's README file.

### Executing Modules
In order for modules to beexecuted (not debugged) they will need to be "patched" or installed. For more information on this see the AnsibleModulePatcher project's README.

## Ansible Bugs and Workarounds

### Timer expired after 10 seconds when gather facts #43884
A bug was discovered in which ansible would timeout trying to gather facts. This timeout would cause the playbook to fail.
https://github.com/ansible/ansible/issues/43884

This is important to consider because it affects the AnsibleUtility's ability to test playbooks.

#### Affected Versions
I have only tested this library on a limited number of installations. AFAIK the following are affected:

| OS       | Version  |
|----------|-------------|
|CentOS|2.7.8        |

If you try to debug a module or run a module which gathers facts, you may see the following output from ansible.

```
TASK [Gathering Facts] ******************************************************************************************************************************************************
task path: /tmp/test_FKRXW92PUI/playbook.yml:2
<localhost> ESTABLISH LOCAL CONNECTION FOR USER: root
<localhost> EXEC /bin/sh -c 'echo ~root && sleep 0'
<localhost> EXEC /bin/sh -c '( umask 77 && mkdir -p "` echo /root/.ansible/tmp/ansible-tmp-1552432637.3746383-261539199569263 `" && echo ansible-tmp-1552432637.3746383-261539199569263="` echo /root/.ansible/tmp/ansible-tmp-1552432637.3746383-261539199569263 `" ) && sleep 0'
Using module file /usr/local/lib/python3.6/site-packages/ansible/modules/system/setup.py
<localhost> PUT /root/.ansible/tmp/ansible-local-2544qwxim7w6/tmpomw0z5f5 TO /root/.ansible/tmp/ansible-tmp-1552432637.3746383-261539199569263/AnsiballZ_setup.py
<localhost> EXEC /bin/sh -c 'chmod u+x /root/.ansible/tmp/ansible-tmp-1552432637.3746383-261539199569263/ /root/.ansible/tmp/ansible-tmp-1552432637.3746383-261539199569263/AnsiballZ_setup.py && sleep 0'
<localhost> EXEC /bin/sh -c '/usr/bin/python /root/.ansible/tmp/ansible-tmp-1552432637.3746383-261539199569263/AnsiballZ_setup.py && sleep 0'
The full traceback is:
Traceback (most recent call last):
  File "/tmp/ansible_setup_payload_gk6KOE/ansible_setup_payload.zip/ansible/module_utils/basic.py", line 2848, in run_command
    cmd = subprocess.Popen(args, **kwargs)
  File "/usr/lib64/python2.7/subprocess.py", line 711, in __init__
    errread, errwrite)
  File "/usr/lib64/python2.7/subprocess.py", line 1308, in _execute_child
    data = _eintr_retry_call(os.read, errpipe_read, 1048576)
  File "/usr/lib64/python2.7/subprocess.py", line 478, in _eintr_retry_call
    return func(*args)
  File "/tmp/ansible_setup_payload_gk6KOE/ansible_setup_payload.zip/ansible/module_utils/facts/timeout.py", line 37, in _handle_timeout
    raise TimeoutError(msg)
TimeoutError: Timer expired after 10 seconds

fatal: [localhost]: FAILED! => {
    "changed": false,
    "cmd": "/usr/sbin/udevadm info --query property --name /dev/sda3",
    "invocation": {
        "module_args": {
            "fact_path": "/etc/ansible/facts.d",
            "filter": "*",
            "gather_subset": [
                "all"
            ],
            "gather_timeout": 10
        }
    },
    "msg": "Timer expired after 10 seconds",
    "rc": 257
}
	to retry, use: --limit @/tmp/test_FKRXW92PUI/playbook.retry
```

The workaround for this is to instruct ansible to gather a minimal set of facts.

This can be done by modifying the `/etc/ansible/ansible.cfg` and setting `gather_subset = !all`

This was discussed here: https://stackoverflow.com/questions/52174866/ansible-playbook-timer-expired-after-10-seconds-only-on-some-nodes-but-works-jus
