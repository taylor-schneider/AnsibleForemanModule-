import yaml
import os
import json

from unittest import TestCase
from AnsibleForemanModule import AnsibleForemanModule
from AnsibleForemanModule.Tests.AnsibleModuleTester.AnsibleModuleTester.AnsibleUtilities.AnsibleUtility import AnsibleUtility
from AnsibleForemanModule.Tests.AnsibleModuleTester.AnsibleModuleTester.AnsibleUtilities.ContextManager_sys_argv import ContextManager_sys_argv
from AnsibleForemanModule.Tests.AnsibleModuleTester.AnsibleModuleTester.AnsibleUtilities.ContextManager_StdioCapture import ContextManager_StdioCapture



class Test_AnsibleFormanModule(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = "admin"
        self.password = "password"
        self.apiUrl = "https://15.4.7.1"
        self.verifySsl = False
        self.moduleName = "AnsibleForemanModule"

        testsDir = os.path.dirname(os.path.realpath(__file__))
        ansibleForemanModuleDir = os.path.dirname(testsDir)
        self.modulePath = ansibleForemanModuleDir + "/" + self.moduleName + ".py"

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
{5}
            """

        return playbookYaml

    def _DesiredStateToPlaybookYaml(self, desiredState):

        desiredStateYaml = yaml.dump(desiredState, default_flow_style=False)
        paddedYaml = ""
        for line in desiredStateYaml.split("\n"):
            paddedYaml += "              " + line + "\n"
        return paddedYaml

    def _GeneratePlaybook(self, moduleName, apiUrl, username, password, verifySsl, desiredState):

        template = self._PlaybookTemplate()

        paddedDesiredStateYaml = self._DesiredStateToPlaybookYaml(desiredState)

        playbook = template.format(moduleName, apiUrl, username, password, verifySsl, paddedDesiredStateYaml)
        return playbook

    def test_Main_EnsureEnvironmentExists_Success(self):
        apiEndpoint = "/api/environments"
        httpMethod = "post"
        desiredState =  {
            "environment": {
                "name": "some_environment"
            }
        }

        playbookYaml = self._GeneratePlaybook(
            self.moduleName,
            self.apiUrl,
            self.username,
            self.password,
            self.verifySsl,
            apiEndpoint,
            httpMethod,
            desiredState)

        AnsibleUtility.RunModuleUsingPlaybook(self.moduleName, self.modulePath, playbookYaml)

    def test__EnsureEnvironmentAbsent_Success_DoesNotExist(self):

        recordName = "test__EnsureEnvironmentAbsent_Success_DoesNotExist"
        apiEndpoint = "/api/environments"
        httpMethod = "post"
        desiredState =  {
            "environment": {
                "name": recordName,
                "state": "absent"
            }
        }

        playbookYaml = self._GeneratePlaybook(
            self.moduleName,
            self.apiUrl,
            self.username,
            self.password,
            self.verifySsl,
            desiredState)

        moduleArgsDict = AnsibleUtility.GetModuleArgsDictFromYaml(self.moduleName, playbookYaml)
        jsonString = AnsibleUtility.GenerateJsonForPlaybookYaml(playbookYaml, self.moduleName, moduleArgsDict)

        # Mock the sys args with the json
        mockedSysArgs = ["ThisShouldBeThePythonFileNameButWeDontCare.py",  jsonString]

        # Run the module, get the results
        result = AnsibleUtility.RunModuleUsingPlaybook(self.moduleName, self.modulePath, playbookYaml)

        # Check the results
        self.assertEqual(result["changed"], False)
        self.assertFalse("modifiedRecord" in result.keys())