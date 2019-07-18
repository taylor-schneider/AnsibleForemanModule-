import logging
import os
from unittest import TestCase
from AnsibleModuleTester.TestingUtilities import AnsibleUtility
from functional_tests.ForemanAnsibleModuleTestCase import ForemanAnsinbleModuleTestCase

# Configure logging format and level
logFormat = '%(asctime)s,%(msecs)d %(levelname)-8s [%(module)s:%(funcName)s():%(lineno)d] %(message)s'

logging.basicConfig(format=logFormat,
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class Test_CreatePxeBootHost_CentOS(ForemanAnsinbleModuleTestCase):


    def __init__(self, *args, **kwargs):

        self.creationPlaybookName = os.path.join("XCP-ng", "CreateXcpngPxeBootEnvironment.yaml")
        self.destructionPlaybookName = os.path.join("XCP-ng", "DestroyForemanXcpngSPxeBootEnvironmentPlaybook.yaml")

        super().__init__(*args, **kwargs)

    def test_CreatePxeBootHost_Xcpng_Debug(self):

        self.tasksToDebug = "all"

        super()._CreatePxeBootHost_Debug()


    def test_CreatePxeBootHost_CentOS_NoDebug(self):

        super()._CreatePxeBootHost_NoDebug()

    def test_DestroyPxeBootHost_CentOS_Debug(self):

        # Run the playbook
        self.tasksToDebug = [
            "Destroy the PXE Boot Host"

            , "UnLink the PXE Operating System with the provisioning templates"
            , "Unlink the PXE Boot Partitioning Table with the PXE Operating System"
            , "Delete PXE Boot Partitioning Table"
            , "Unlink the PXE PXELinux Provisioning Template with the PXE Operating System"

            , "Un-Set the default Provisioning Template for the PXE Operating system"
            , "Un-Set the default Answer File for the PXE Operating system"

            , "Delete the PXE PXELinux Provisioning Template"
            , "Unlink the PXE OS Answer File with the PXE Operating System"
            , "Delete PXE OS Answer File"

            , "Delete PXE Boot Installation Media"
            , "Delete PXE Operating System"

            , "Unlink PXE Boot Subnet from the smart proxy"
            , "Delete PXE Boot Subnet"
            , "Unlink PXE Boot Domain with the SMART Proxy"
            , "Delete PXE Boot Domain"
        ]

        super()._DestroyPxeBootHost_Debug()

    def test_DestroyPxeBootHost_CentOS_NoDebug(self):

        super()._DestroyPxeBootHost_NoDebug()