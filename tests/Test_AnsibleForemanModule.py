import yaml
import os
import logging
import json
from unittest import TestCase
from AnsibleModuleTester.TestingUtilities import AnsibleUtility
from ForemanApiWrapper.RecordUtilities import RecordComparison
from ForemanApiWrapper.RecordUtilities import ForemanApiRecord
from ForemanApiWrapper.ForemanApiUtilities.ForemanApiWrapper import ForemanApiWrapper

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class Test_AnsibleFormanModule(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = "admin"
        self.password = "password"
        self.apiUrl = "https://15.4.5.1"
        self.verifySsl = False
        self.api_wrapper = ForemanApiWrapper(self.username, self.password, self.apiUrl, self.verifySsl)

        self.moduleName = "AnsibleForemanModule"
        self.taskName = "This is my task to execute my module"

        testsDir = os.path.dirname(os.path.realpath(__file__))
        rootDir = os.path.dirname(testsDir)
        self.modulePath = rootDir + "/ansible/modules/"

    def _playbook_template(self):

        # This function will generate a playbook to run a single play
        # The play will have a single task
        # The task will use the AnsibleForemanModule

        playbookYaml = """
        - hosts: localhost
          remote_user: root
          tasks:
          - name : {0}
            {1}:
              apiUrl : '{2}'
              username : '{3}'
              password : '{4}'
              verifySsl: {5}          
              record:
{6}
              state: {7}"""

        return playbookYaml

    def _generate_padded_yaml_for_desired_state(self, desiredState):

        desiredStateYaml = yaml.dump(desiredState, default_flow_style=False)
        paddedYaml = ""
        for line in desiredStateYaml.split("\n"):
            paddedYaml += "                " + line + "\n"
        return paddedYaml

    def _generate_playbook(self, moduleName, apiUrl, username, password, verifySsl, record, state):

        template = self._playbook_template()

        paddedRecordYaml = self._generate_padded_yaml_for_desired_state(record)
        paddedRecordYaml = paddedRecordYaml.rstrip()

        playbook = template.format(self.taskName, moduleName, apiUrl, username, password, verifySsl, paddedRecordYaml, state)
        return playbook

    def _run_ansible_forman_module(self, record, state):

        playbookYaml = self._generate_playbook(
            self.moduleName,
            self.apiUrl,
            self.username,
            self.password,
            self.verifySsl,
            record,
            state)

        # Run the module, get the results
        cleanup = True
        result = AnsibleUtility.test_playbook(playbookYaml, [self.taskName], cleanup, [self.modulePath])

        return result

    def test__Ensure_Environment_Present_Success_DoesNotExist(self):

        # Create the record for the playbook
        recordName = "test__Ensure_Environment_Present_Success_DoesNotExist"
        recortType = "environment"
        minimal_record = {
            "name": recordName
        }
        playbook_record = {
            recortType: minimal_record
        }
        desired_state = "present"

        try:

            # Run the playbook to create the record
            playbook_results = self._run_ansible_forman_module(playbook_record, desired_state)
            play_results = playbook_results[0]
            task_results = play_results[self.taskName]
            record_modification_receipt = json.loads(task_results)
            actual_record = record_modification_receipt["actual_record"]

            # Check the results and make sure the record did not exist originally
            self.assertTrue(record_modification_receipt["changed"])

            record_identifier_field, record_identifier = ForemanApiRecord.get_identifier_from_record(playbook_record)
            record_type = ForemanApiRecord.get_record_type_from_record(playbook_record)
            ForemanApiRecord.confirm_modified_record_identity(record_identifier, record_type, actual_record)

        finally:
            # Cleanup after the test
            desired_state = "absent"
            self._run_ansible_forman_module(playbook_record, desired_state)

    def test__Ensure_Environment_Absent_Success_DoesNotExist(self):

        recordName = "test__Ensure_Environment_Absent_Success_DoesNotExist"
        recortType = "environment"
        minimal_record = {
            "name": recordName
        }
        playbook_record = {
            recortType: minimal_record
        }
        desired_state = "absent"

        playbook_results = self._run_ansible_forman_module(playbook_record, desired_state)
        play_results = playbook_results[0]
        task_results = play_results[self.taskName]
        record_modification_receipt = json.loads(task_results)
        actual_record = record_modification_receipt["actual_record"]

        # Check the results
        self.assertFalse(record_modification_receipt["changed"])
        self.assertIsNone(actual_record)

    def test__Ensure_Environment_Absent_Success_Deleted(self):

        recordName = "test__Ensure_Environment_Absent_Success_Deleted"
        recortType = "environment"
        minimal_record = {
            "name": recordName
        }
        playbook_record = {
            recortType: minimal_record
        }
        desired_state = "present"

        try:
            # Delete the record if it exists
            self._run_ansible_forman_module(playbook_record, "absent")

            # Create the record
            playbook_results = self._run_ansible_forman_module(playbook_record, desired_state)
            play_results = playbook_results[0]
            task_results = play_results[self.taskName]
            record_modification_receipt = json.loads(task_results)
            actual_record = record_modification_receipt["actual_record"]

            # Check that it was created
            record_identifier_field, record_identifier = ForemanApiRecord.get_identifier_from_record(playbook_record)
            record_type = ForemanApiRecord.get_record_type_from_record(playbook_record)
            ForemanApiRecord.confirm_modified_record_identity(record_identifier, record_type, actual_record)

        finally:
            # Cleanup after the test
             self._run_ansible_forman_module(playbook_record, "absent")

    def test__Adhoc_Playbook(self):

        playbookYaml = """
- hosts: localhost
  remote_user: root
  tasks:
    - name: This is my task to execute my module
      AnsibleForemanModule:
        apiUrl: https://15.4.5.1
        username: admin
        password: password
        verifySsl: false
        record:
          operatingsystem:
            architecture_ids: []
            config_template_ids: []
            description: CentOS Operating System
            family: Redhat
            major: 7
            medium_ids: []
            minor: 8.2003
            name: CentOS
            password_hash: SHA256
            provisioning_template_ids: []
            ptable_ids: []
        state: present
"""

        playbookYaml = """
        - hosts: localhost
          remote_user: root
          tasks:
            - name: This is my task to execute my module
              AnsibleForemanModule:
                apiUrl: https://15.4.5.1
                username: admin
                password: password
                verifySsl: false
                record:
                  host:
                    id: 3
                state: absent
        """

        # Run the module, get the results
        cleanup = True
        result = AnsibleUtility.test_playbook(playbookYaml, [self.taskName], cleanup, [self.modulePath])

        return result
