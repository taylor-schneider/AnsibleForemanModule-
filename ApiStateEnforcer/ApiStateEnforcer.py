from ApiStateEnforcer.ApiStateEnforcerException import ApiStateEnforcerException

class ApiStateEnforcer():

    def __init__(self, apiWrapper):
        self.apiWrapper = apiWrapper

    SetCompareFailedErrorMessage = "The record returned from the set operation did not represent the specified minimal state."

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

            actualState = self.apiWrapper.MakeApiCall(setUrl, httpMethod, minimalState, headers)

            minimalStateExists = self.Compare(minimalState, actualState)

            if not minimalStateExists:
                raise ApiStateEnforcerException(self.SetCompareFailedErrorMessage, minimalState, actualState)

            return actualState

        except Exception as e:
            raise Exception("An error occurred while setting state.") from e

    def Delete(self, deleteUrl, httpMethod, httpMethodParameters,  minimalState):

        # It looks like a delete is simply setting some value to nothing
        # Once deleted, a record for the deleted element will be returned
        # This slightly changes things from the Set() function of this class
        # Here, our delete function will accept parameters and then enforce a minimal state

        try:
            actualState = self.apiWrapper.MakeApiCall(deleteUrl, httpMethod, httpMethodParameters, None)

            minimalStateExists = self.Compare(minimalState, actualState)

            if not minimalStateExists:
                raise ApiStateEnforcerException(self.SetCompareFailedErrorMessage, minimalState, actualState)

            return actualState

        except Exception as e:
            raise Exception("An error occurred while deleting state.") from e


