import yaml
import os
import logging
from unittest import TestCase
from AnsibleModuleTester.TestingUtilities import AnsibleUtility


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class Test_AnsibleFormanModule(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = "admin"
        self.password = "password"
        self.apiUrl = "https://15.4.7.1"
        self.verifySsl = False
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
              action: provision
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

        recordName = "test__Ensure_Environment_Present_Success_DoesNotExist"
        recortType = "environment"
        record =  {
            recortType: {
                "name": recordName
            }
        }
        state = "present"

        try:
            result = self._run_ansible_forman_module(record, state)

            # Check the results
            #self.assertTrue(result["changed"])
            #self.assertTrue("modifiedRecord" in result.keys())
        finally:
            pass
            # Now delete this record
            state =  "absent"
            result = self._run_ansible_forman_module(record, state)
            #self.assertTrue(result["changed"])
            #self.assertTrue("modifiedRecord" in result.keys())

    def test__Ensure_Environment_Absent_Success_DoesNotExist(self):
        recordName = "test__Ensure_Environment_Absent_Success_DoesNotExist"
        recortType = "environment"
        desiredState = {
            recortType: {
                "name": recordName,
                "state": "absent"
            }
        }

        result = self._run_ansible_forman_module(desiredState, "absent")

        # Check the results
        self.assertFalse(result["changed"])
        self.assertFalse("modifiedRecord" in result.keys())

    def test__Ensure_Environment_Absent_Success_Deleted(self):

        recordName = "test__Ensure_Environment_Absent_Success_Deleted"
        recortType = "environment"
        desiredState =  {
            recortType: {
                "name": recordName,
                "state": "present"
            }
        }

        playbookResult = self._run_ansible_forman_module(desiredState, "absent")
        playResult = playbookResult[0]
        taskResult = playResult[self.taskName]

        # Check the results
        self.assertTrue(taskResult["changed"])
        self.assertTrue("modifiedRecord" in taskResult.keys())

        # Now delete this record
        desiredState[recortType]["state"] = "absent"
        result = self._run_ansible_forman_module(desiredState)
        self.assertTrue(result["changed"])
        self.assertTrue("modifiedRecord" in result.keys())


