import yaml
import os
import logging

from unittest import TestCase

from AnsibleModuleTester.AnsibleUtilities.AnsibleUtility import AnsibleUtility


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

        testsDir = os.path.dirname(os.path.realpath(__file__))
        rootDir = os.path.dirname(testsDir)
        self.modulePath = rootDir + "/ansible/library/"

    def _PlaybookTemplate(self):
        playbookYaml = """
        - hosts: localhost
          remote_user: root
          tasks:
          - set_fact: my_global_var='hello'
          - name: "Re-run setup to use custom facts"
            setup: ~
          - name : "This is my task to execute my module"
            {0}:
              apiUrl : '{1}'
              username : '{2}'
              password : '{3}'
              verifySsl: {4}          
              record:
{5}
              action: provision
              state: {6}"""

        return playbookYaml

    def _DesiredStateToPlaybookYaml(self, desiredState):

        desiredStateYaml = yaml.dump(desiredState, default_flow_style=False)
        paddedYaml = ""
        for line in desiredStateYaml.split("\n"):
            paddedYaml += "                " + line + "\n"
        return paddedYaml

    def _GeneratePlaybook(self, moduleName, apiUrl, username, password, verifySsl, record, state):

        template = self._PlaybookTemplate()

        paddedRecordYaml = self._DesiredStateToPlaybookYaml(record)

        paddedRecordYaml = paddedRecordYaml.rstrip()

        playbook = template.format(moduleName, apiUrl, username, password, verifySsl, paddedRecordYaml, state)
        return playbook

    def _RunModuleGetResult(self, record, state):

        playbookYaml = self._GeneratePlaybook(
            self.moduleName,
            self.apiUrl,
            self.username,
            self.password,
            self.verifySsl,
            record,
            state)

        # Run the module, get the results
        result = AnsibleUtility.DebugPlaybook(playbookYaml, ["This is my task to execute my module"], True, [self.modulePath])

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
            result = self._RunModuleGetResult(record, state)

            # Check the results
            #self.assertTrue(result["changed"])
            #self.assertTrue("modifiedRecord" in result.keys())
        finally:
            pass
            # Now delete this record
            state =  "absent"
            result = self._RunModuleGetResult(record, state)
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

        result = self._RunModuleGetResult(desiredState)

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

        result = self._RunModuleGetResult(desiredState)

        # Check the results
        self.assertTrue(result["changed"])
        self.assertTrue("modifiedRecord" in result.keys())

        # Now delete this record
        desiredState[recortType]["state"] = "absent"
        result = self._RunModuleGetResult(desiredState)
        self.assertTrue(result["changed"])
        self.assertTrue("modifiedRecord" in result.keys())


