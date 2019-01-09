from unittest import TestCase

from ForemanApiWrapper.ForemanApiWrapper import ForemanApiWrapper
from AnsibleForemanModule.ApiStateEnforcer.ApiStateEnforcer import ApiStateEnforcer

class Test_ApiStateEnforcer(TestCase):

    def __init__(self, *args, **kwargs):
        super(Test_ApiStateEnforcer, self).__init__(*args, **kwargs)
        self.username = "admin"
        self.password = "password"
        self.url = "https://15.4.7.1"
        self.verifySsl = False

    def test_Check_RecordExists_Success(self):

        apiWrapper = ForemanApiWrapper(self.username, self.password, self.url, self.verifySsl)
        apiStateEnforcer = ApiStateEnforcer(apiWrapper)

        endpoint = "/api/environments/some_environment"
        method = "get"

        jsonState = apiStateEnforcer.Check(endpoint, method)

    def test_Compare_MinimalStateExists_Success(self):

        apiWrapper = ForemanApiWrapper(self.username, self.password, self.url, self.verifySsl)
        apiStateEnforcer = ApiStateEnforcer(apiWrapper)

        endpoint = "/api/environments"
        method = "get"

        actualState = apiStateEnforcer.Check(endpoint, method)
        total = actualState["total"]

        minimalState = { "total" : total}

        minimalStateExists = apiStateEnforcer.Compare(minimalState, actualState)

        self.assertTrue(minimalStateExists)

    def test_Set_CreateRecord_Success(self):

        apiWrapper = ForemanApiWrapper(self.username, self.password, self.url, self.verifySsl)
        apiStateEnforcer = ApiStateEnforcer(apiWrapper)

        endpoint = "/api/environments"
        method = "post"
        minimalState =  {
            "environment": {
                "name": "some_environment"
            }
        }

        actualState = apiStateEnforcer.Set(endpoint, method, minimalState)

        self.assertIsNotNone(actualState)
        self.assertEqual(type(actualState), dict)

    def test_Delete_DeleteRecord_Success(self):

        apiWrapper = ForemanApiWrapper(self.username, self.password, self.url, self.verifySsl)
        apiStateEnforcer = ApiStateEnforcer(apiWrapper)

        environmentName = "some_environment"

        endpoint = "/api/environments/{0}".format(environmentName)
        method = "delete"
        minimalState = {
            "name": environmentName,
        }

        actualState = apiStateEnforcer.Delete(endpoint, method, minimalState)

        self.assertIsNotNone(actualState)
        self.assertEqual(type(actualState), dict)