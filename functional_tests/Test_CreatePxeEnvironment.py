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
        self.creationPlaybookName = "CreateForemanCentOSPxeBootEnvironmentPlaybook.yaml"
        self.destructionPlaybookName = "DestoryForemanCentOSPxeBootEnvironmentPlaybook.yaml"

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

    def test_CreatePxeEnvironment_Debug(self):

        playbookYaml = self._getCreationPlaybookYaml()

        # Run the playbook
        tasksToDebug = [
            "Get SMART Proxy info"
            , "Create a Domain for the PXE environment"
            , "Create a Subnet for the tftp PXE environment"

            , "Create an Architecture for the PXE environment"
            , "Create an Installation for the PXE environment"
            , "Create an Operating System for the PXE environment"

            , "Download PXELinux Provisioning Template"
            , "Download Answer File Template"

            , "Create the PXELinux Provisioning Template and link it with the PXE Operating System"
            , "Create the Answer File and link it with the PXE Operating System"

            , "Link the Operating System with the Partition Table, Provisioning Tamplate, and Answer File"
            , "Link the PXE PXELinux Provisioning Template with the Operating System"
            , "Link the Answer File with the Operating System"
            , "Set the default Provisioning Template for the PXE Operating system"
            , "Set the default Answer File for the PXE Operating system"

            ,  "Create the PXE Boot Host"
        ]

        # As we are debugging the tasks, if a task fails an exception will be raised
        playbook_results = AnsibleUtility.test_playbook(playbookYaml, tasksToDebug)


    def test_DestroyPxeEnvironment_Debug(self):

        playbookYaml = self._getDestructionPlaybookYaml()

        # Run the playbook
        tasksToDebug = [
            "UnLink the PXE Operating System with the provisioning templates",
            "Unlink the PXE Boot Partitioning Table with the PXE Operating System",
            "Delete PXE Boot Partitioning Table",
            "Unlink the PXE PXELinux Provisioning Template with the PXE Operating System",
            "Delete the PXE PXELinux Provisioning Template",
            "Delete PXE OS Answer File",
            "Unlink the PXE OS Answer File with the PXE Operating System",
            "Delete the default Provisioning Template for the PXE Operating system",

            "Delete PXE Operating System",
            "Unlink PXE Boot Subnet from the smart proxy",
            "Delete PXE Boot Subnet",
            "Unlink PXE Boot Domain with the SMART Proxy",
            "Delete PXE Boot Domain",
            "Delete PXE Boot Architecture",
            "Delete PXE Boot Installation Media"

        ]

        playbook_results = AnsibleUtility.test_playbook(playbookYaml, tasksToDebug)


    def test_CreatePxeEnvironment_NoDebug(self):

        playbookYaml = self._getCreationPlaybookYaml()

        # Run the playbook
        tasksToDebug = []
        tasksToDebug.append("Create PXE Operating system")

        playbook_results = AnsibleUtility.test_playbook(playbookYaml, tasksToDebug)
