from AnsibleForemanModule.ApiStateEnforcer.StateComparisonException import StateComparisonException
from AnsibleForemanModule.ApiStateEnforcer import ModifiedRecordMismatchException
from ForemanApiWrapper.ForemanApiWrapper.ForemanApiCallException import ForemanApiCallException

class ApiStateEnforcer():

    ModifiedRecordMismatchMessage = "The modified record's 'name' and 'id' fields did not match those supplied in the api url."

    def __init__(self, apiWrapper):
        self.apiWrapper = apiWrapper

    def Check(self, checkUrl, httpMethod):

        return self.apiWrapper.MakeApiCall(checkUrl, httpMethod)

    def Compare(self, minimalState, actualState):

        # This function will return true or false based on whether or not the
        # actual state represents the minimal state
        #       Ie. All the keys/values in minimal state exist in actual

        # Check that the two objects are the same type
        if type(minimalState) != type(actualState):
            return False

        # Now that we know the objects are the same, we can compare

        # Certain non primitives need to be handled separately

        # Dictionaries are an axample of this
        if isinstance(minimalState, dict):
            actualKeys = list(actualState.keys())

            # If a key is missing that is a dead givaway
            for key,value in minimalState.items():
                if key not in actualKeys:
                    return False

                # Call this function recursively
                # Return false if any of the keys dont match

                actualValue = actualState[key]
                minimalValue = minimalState[key]

                comparisonResult = self.Compare(minimalValue, actualValue)
                if not comparisonResult:
                    return False

            # If we got here without exiting, we match!
            return True

        # lists and other objects should compare just fine
        else:
            return minimalState == actualState

    @staticmethod
    def _GetNameOrIdFromRecord(record):

        # The state will show what an object should look like
        # For example:
        #    {
        #        "name": "some_environment"
        #    }

        if "name" in record.keys():
            return record["name"]
        if "id" in record.keys():
            return record["id"]
        raise Exception("Could not determine name or id from record.")

    @staticmethod
    def _ConfirmModifiedRecordIdentity(nameOrId, record):
        if "name" in record.keys():
            if record["name"] == nameOrId:
                return True
        if "id" in record.keys():
            if record["id"] == nameOrId:
                return True
        return False

    def Set(self, setUrl, httpMethod, minimalState):

        try:
            # Foreman's API specifies that put and post api calls must set the Content-type header
            # If we dont, we will get an exception as follows:
            #       Exception.args[0]:
            #           '415 Client Error: Unsupported Media Type for url: https://15.4.7.1/api/environments'
            #
            #       response._content:
            #           b'{\n  "error": {"message":"\'Content-Type: \' is unsupported in API v2 for POST and PUT requests. Please use \'Content-Type: application/json\'."}\n}\n'

            headers = {}
            if httpMethod.lower() in ["put", "post"]:
                headers = {'Content-type': 'application/json'}

            # When a record is created/updated, the record is returned as the result of the api call
            # We will need to verify that the record being returned corresponds to the record in question
            nameOrId = ApiStateEnforcer._GetNameOrIdFromRecord(minimalState)
            record = self.apiWrapper.MakeApiCall(setUrl, httpMethod, minimalState, headers)
            recordMatch = ApiStateEnforcer._ConfirmModifiedRecordIdentity(nameOrId, record)

            if not recordMatch:
                raise ModifiedRecordMismatchException(self.ModifiedRecordMismatchMessage, setUrl, httpMethod, minimalState, record)

            return record

        except Exception as e:
            raise Exception("An error occurred while setting state.") from e

    def Delete(self, deleteUrl, httpMethod, minimalState):

        # It looks like a delete is simply setting some value to nothing
        # Once deleted, a record for the deleted element will be returned
        # This slightly changes things from the Set() function of this class
        # Here, our delete function will delete the record and then ensure
        # that the deleted record matches the url supplied

        try:
            record = self.apiWrapper.MakeApiCall(deleteUrl, httpMethod, minimalState, None)

            # When a record is created/updated, the record is returned as the result of the api call
            # We will need to verify that the record being returned corresponds to the record in question

            # In the case of the delete, the name/id is stored as the suffix in the url
            nameOrId = deleteUrl.split("/")[-1]
            recordMatch = ApiStateEnforcer._ConfirmModifiedRecordIdentity(nameOrId, record)

            if not recordMatch:
                raise ModifiedRecordMismatchException(self.ModifiedRecordMismatchMessage, deleteUrl, httpMethod, minimalState, record)

            return record

        except Exception as e:
            raise Exception("An error occurred while deleting state.") from e

    @staticmethod
    def _DetermineHttpEndpoint(recordType, nameOrId):
        return "/api/{0}s/{1}".format(recordType, nameOrId)

    def EnsureState(self, recordType, desiredState, minimalRecordState):

        try:
            if desiredState.lower() not in ["present", "absent"]:
                raise Exception("The specified desired state '{0}' was not valid.".format(desiredState))

            # Gather some information for the api
            nameOrId = ApiStateEnforcer._GetNameOrIdFromRecord(minimalRecordState)
            httpEndpoint = ApiStateEnforcer._DetermineHttpEndpoint(recordType, nameOrId)

            # Get the current state
            # If the api throws a 404, the record does not exist
            # Otherwise it does exist
            actualRecordState = None
            try:
                actualRecordState = self.Check(httpEndpoint, "get")
            except ForemanApiCallException as e:
                if e.results.status_code == 404:
                    pass

            # Determine what change is required (if any)
            changeRequired = True
            if desiredState.lower() == "present":
                changeRequired = self.Compare(minimalRecordState, actualRecordState)
            elif desiredState.lower() == "absent" and not actualRecordState:
                changeRequired = False

            # If not change is required, our work is done
            if not changeRequired:
                return { "changed": False }

            # Do the change
            modifiedRecord = None
            if desiredState.lower is "present":
                modifiedRecord = self.Set(httpEndpoint, "post", minimalRecordState)
            else:
                modifiedRecord = self.Delete(httpEndpoint,"delete", minimalRecordState)

            # Return the results
            return {
                "changed" : changeRequired,
                "modifiedRecord" : modifiedRecord
            }

        except Exception as e:
            raise Exception("An error occurred while ensuring the api state.") from e

