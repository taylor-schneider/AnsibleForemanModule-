import logging
import os
import json

from unittest import TestCase
from AnsibleModuleTester.TestingUtilities import AnsibleUtility

logFormat = '%(asctime)s,%(msecs)d %(levelname)-8s [%(module)s:%(funcName)s():%(lineno)d] %(message)s'

logging.basicConfig(format=logFormat,
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class Test_CreatePxeEnvironment(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = "admin"
        self.password = "password"
        self.apiUrl = "https://15.4.7.1"
        self.verifySsl = False
        self.moduleName = "AnsibleForemanModule"
        self.creationPlaybookName = "CreateXcpngPxeBootClientPlaybook.yaml"
        self.destructionPlaybookName = "DestroyXcpngPxeBootClientPlaybook.yaml"

        testsDir = os.path.dirname(os.path.realpath(__file__))
        projectDir = os.path.dirname(testsDir)
        self.creationPlayboookPath = projectDir + "/playbooks/" + self.creationPlaybookName
        self.destructionPlaybookPath = projectDir + "/playbooks/" + self.destructionPlaybookName

        self.modulePath = projectDir + "/Modules/AnsibleForemanModule/AnsibleForemanModule" # + self.moduleName + ".py"

    def _getCreationPlaybookYaml(self):
        # Get the playbook yaml
        playbookYaml = None
        with open(self.creationPlayboookPath, 'r') as file:
            playbookYaml = file.read()
        return playbookYaml

    def _getDestructionPlaybookYaml(self):
        # Get the playbook yaml
        playbookYaml = None
        with open(self.destructionPlaybookPath, 'r') as file:
            playbookYaml = file.read()
        return playbookYaml

    def test_CreatePxeclient_NoDebug(self):

        playbookYaml = self._getCreationPlaybookYaml()

        # As we are debugging the tasks, if a task fails an exception will be raised
        playbook_results = AnsibleUtility.run_playbook(playbookYaml)

