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

class ForemanAnsinbleModuleTestCase(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Parameters for connecting to Foreman
        self.username = "admin"
        self.password = "password"
        self.apiUrl = "https://15.4.7.1"
        self.verifySsl = False

        # Parameters for playbooks
        testsDir = os.path.dirname(os.path.realpath(__file__))
        projectDir = os.path.dirname(testsDir)
        playbooksDir = os.path.join(projectDir, "playbooks")
        if not hasattr(self, "creationPlaybookName") or not self.creationPlaybookName:
            self.creationPlaybookName = "playbook_name.yaml"
        if not hasattr(self, "destructionPlaybookName") or not self.destructionPlaybookName:
            self.destructionPlaybookName = "playbook_name.yaml"
        self.creationPlayboookPath = os.path.join(playbooksDir, self.creationPlaybookName)
        self.destructionPlaybookPath = os.path.join(playbooksDir, self.destructionPlaybookName)

        # Parameters for debugging the playbook
        if not hasattr(self, "tasksToDebug") or not self.tasksToDebug:
            self.tasksToDebug = []

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

    def _CreatePxeBootHost_Debug(self):

        playbookYaml = self._getCreationPlaybookYaml()

        # As we are debugging the tasks, if a task fails an exception will be raised
        playbook_results = AnsibleUtility.test_playbook(playbookYaml, self.tasksToDebug)

    def _CreatePxeBootHost_NoDebug(self):

        playbookYaml = self._getCreationPlaybookYaml()
        playbook_results = AnsibleUtility.run_playbook(playbookYaml)

    def _DestroyPxeBootHost_Debug(self):

        playbookYaml = self._getDestructionPlaybookYaml()

        # As we are debugging the tasks, if a task fails an exception will be raised
        playbook_results = AnsibleUtility.test_playbook(playbookYaml, self.tasksToDebug)

    def _DestroyPxeBootHost_NoDebug(self):

        playbookYaml = self._getDestructionPlaybookYaml()
        playbook_results = AnsibleUtility.run_playbook(playbookYaml)