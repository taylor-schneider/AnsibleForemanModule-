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

        self.creationPlaybookName = os.path.join("CentOS", "CreateForemanCentOSPxeBootEnvironmentPlaybook.yaml")
        self.destructionPlaybookName = os.path.join("CentOS", "DestroyForemanCentOSPxeBootEnvironmentPlaybook.yaml")

        super().__init__(*args, **kwargs)

    def test_CreatePxeBootHost_CentOS_Debug(self):

        self.tasksToDebug = "all"
        #self.tasksToDebug = ["Delete the default Provisioning Template for the PXE Operating system"]

        super()._CreatePxeBootHost_Debug()

    def test_CreatePxeBootHost_CentOS_NoDebug(self):

        super()._CreatePxeBootHost_NoDebug()

    def test_DestroyPxeBootHost_CentOS_Debug(self):

        # Run the playbook
        self.tasksToDebug = "all"

        super()._DestroyPxeBootHost_Debug()

    def test_DestroyPxeBootHost_CentOS_NoDebug(self):

        super()._DestroyPxeBootHost_NoDebug()