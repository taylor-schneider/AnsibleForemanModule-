import json
import os
from AnsibleForemanModule.ApiStateEnforcer.ModifiedRecordMismatchException import ModifiedRecordMismatchException
from ForemanApiWrapper.ForemanApiWrapper.ForemanApiCallException import ForemanApiCallException
from ForemanApiWrapper.ForemanApiWrapper.ForemanApiWrapper import ForemanApiWrapper

class ApiStateEnforcer():

    StateMismatchMessage = "The actual state did not match the desired state."
    RecordAlreadyAbsentMessage = "Record is already absent."
    MissingRecordMessage =  "Record does not exist and it should."
    ExtraRecordMessage = "Record exists and it should not."

    ModifiedRecordMismatchMessage = "The modified record's 'name' or 'id' fields did not match those supplied in the api url."

    def __init__(self, apiWrapper):
        self.apiWrapper = apiWrapper

    def Check(self, recordType, minimalRecordState):

        nameOrId, nameOrIdValue = ApiStateEnforcer._GetNameOrIdFromRecord(minimalRecordState)
        nameOrIdForUrl = ApiStateEnforcer._FormatNameOrIdForApiUrl(nameOrId, nameOrIdValue)
        endpointSuffix = ApiStateEnforcer._GetApiUrlSuffixForRecordType(recordType)
        checkUrl = "/api/{0}/{1}".format(endpointSuffix, nameOrIdForUrl)
        httpMethod = "GET"

        record =  self.apiWrapper.MakeApiCall(checkUrl, httpMethod)
        return record

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

        possibleKeys = ["name", "id"]
        for key in possibleKeys:
            if key in record.keys():
                return key, record[key]

        raise Exception("Could not determine name or id from record.")

    @staticmethod
    def _GetApiUrlSuffixForRecordType(recordType):
        # Most of the records map directly to the api endpoint
        # for example environment record type maps to the /api/environments endpoint
        # Some record types break this model, and we have a mapping file for this

        # Get the path to the mapping file
        currentFilePath = os.path.realpath(__file__)
        currentDirectory = os.path.dirname(currentFilePath)
        mappingFileDirectory = os.path.join(currentDirectory, "MappingFiles")
        mappingFilePath = os.path.join(mappingFileDirectory, "ApiRecordToUrlSuffixMapping.json")

        # Read the json text from the file
        fileText = None
        with open(mappingFilePath, 'r') as mappingfile:
            fileText = mappingfile.read()

        # Deserialize it into an object
        mappings = json.loads(fileText)

        # Set the default endpoint
        endpointSuffix = "{0}s".format(recordType)

        # Check if the record type is contained in the mapping
        # If it is, override the default endpoint
        if recordType in mappings.keys():
            endpointSuffix = mappings[recordType]

        return endpointSuffix

    @staticmethod
    def _FormatNameOrIdForApiUrl(nameOrId, nameOrIdValue):
        endpoint = nameOrIdValue
        if nameOrId == "id":
            endpoint = ":{0}".format(nameOrIdValue)
        return endpoint

    @staticmethod
    def _ConfirmModifiedRecordIdentity(nameOrId, record):
        if "name" in record.keys():
            if record["name"] == nameOrId:
                return True
        if "id" in record.keys():
            if record["id"] == nameOrId:
                return True
        return False

    @staticmethod
    def _GetApiRecordPropertyNameMappings():
        # This will import and deserialize the json file with the name mappings

        currentFilePath = os.path.realpath(__file__)
        currentDirectory = os.path.dirname(currentFilePath)
        mappingFileDirectory = os.path.join(currentDirectory, "MappingFiles")
        mappingFilePath = os.path.join(mappingFileDirectory, "ApiRecordPropertyNameMappings.json")

        # Read the json text from the file
        fileText = None
        with open(mappingFilePath, 'r') as mappingfile:
            fileText = mappingfile.read()

        # Deserialize it into an object
        mappings = json.loads(fileText)
        return mappings

    @staticmethod
    def _ConvertRecordForApiMethod(httpMethod, recordType, record):

        # Sometimes this method is used in conjunction with the Check method
        # This is problematic:
        #   The check method uses a GET while the update method uses a PUT
        #   The API is inconsistent in the way it represents records and we know
        #   that the record returned by a GET will not always be the same as a PUT
        #   We may need to change some of the names of the properties on the
        #   json object being submitted to the foreman API
        #   These changes are noted in the mapping file
        # An example mapping is as follows:
        # {
        # 	"put" : {
        # 		"subnet" : {
        # 			"domains" : "domain_ids"
        # 		}
        # 	}
        # }

        # Get mappings
        mappings = ApiStateEnforcer._GetApiRecordPropertyNameMappings()

        # If no mapping is defined, we just return the record untouched
        httpMethod = httpMethod.lower()
        recordType = recordType.lower()
        if httpMethod not in mappings.keys():
            return record
        if recordType not in mappings[httpMethod].keys():
            return record

        requiredChanges = mappings[httpMethod][recordType]

        # For each property in the record, make the required changes
        convertedRecord = {}
        for key, value in record.items():
            if key in requiredChanges.keys():
                newKey = requiredChanges[key]
                convertedRecord[newKey] = value
            else:
                convertedRecord[key] = value

        return convertedRecord

    @staticmethod
    def _GetApiCallArguments(recordType, record):
        apiCallArguments = {
            recordType: record
        }
        return apiCallArguments

    def Set(self, recordType, minimalRecordState):

        try:
            nameOrId, nameOrIdValue = ApiStateEnforcer._GetNameOrIdFromRecord(minimalRecordState)
            endpointSuffix = ApiStateEnforcer._GetApiUrlSuffixForRecordType(recordType)
            setUrl = "/api/{0}".format(endpointSuffix)
            httpMethod = "POST"

            headers = ForemanApiWrapper._GetHeadersForHttpMethod(httpMethod)

            # We may need to convert the record based on the API endpoint being used
            # The API is inconsistent in the way it represents data
            recordForPost = ApiStateEnforcer._ConvertRecordForApiMethod(httpMethod, recordType, minimalRecordState)

            # The api call will expect the arguments in a certain form
            apiCallArguments = ApiStateEnforcer._GetApiCallArguments(recordType, recordForPost)

            record = self.apiWrapper.MakeApiCall(setUrl, httpMethod, minimalRecordState, headers)
            # When a record is created/updated, the record is returned as the result of the api call
            # We will need to verify that the record being returned corresponds to the record in question
            recordMatch = ApiStateEnforcer._ConfirmModifiedRecordIdentity(nameOrIdValue, record)

            if not recordMatch:
                raise ModifiedRecordMismatchException(self.ModifiedRecordMismatchMessage, setUrl, httpMethod, minimalRecordState, record)

            return record

        except Exception as e:
            raise Exception("An error occurred while setting state.") from e

    def Update(self, recordType, minimalRecordState):

        try:
            nameOrId, nameOrIdValue = ApiStateEnforcer._GetNameOrIdFromRecord(minimalRecordState)
            nameOrIdForUrl = ApiStateEnforcer._FormatNameOrIdForApiUrl(nameOrId, nameOrIdValue)
            endpointSuffix = ApiStateEnforcer._GetApiUrlSuffixForRecordType(recordType)
            setUrl = "/api/{0}/{1}".format(endpointSuffix, nameOrIdForUrl)
            httpMethod = "PUT"

            # Foreman's API specifies that put and post api calls must set the Content-type header
            # If we dont, we will get an exception as follows:
            #       Exception.args[0]:
            #           '415 Client Error: Unsupported Media Type for url: https://15.4.7.1/api/environments'
            #
            #       response._content:
            #           b'{\n  "error": {"message":"\'Content-Type: \' is unsupported in API v2 for POST and PUT requests. Please use \'Content-Type: application/json\'."}\n}\n'

            headers = ForemanApiWrapper._GetHeadersForHttpMethod(httpMethod)

            # We may need to convert the record based on the API endpoint being used
            # The API is inconsistent in the way it represents data
            recordForPut = ApiStateEnforcer._ConvertRecordForApiMethod(httpMethod, recordType, minimalRecordState)

            # The api call will expect the arguments in a certain form
            apiCallArguments = ApiStateEnforcer._GetApiCallArguments(recordType, recordForPut)
            recordFromPut = self.apiWrapper.MakeApiCall(setUrl, httpMethod, apiCallArguments, headers)

            # We will need to verify that the record being returned corresponds to the record in question
            # We can do this by comparing the nome or id fields on the record returned with
            # The name or id supplied to the API
            recordMatch = ApiStateEnforcer._ConfirmModifiedRecordIdentity(nameOrIdValue, recordFromPut)

            if not recordMatch:
                raise ModifiedRecordMismatchException(self.ModifiedRecordMismatchMessage, setUrl, httpMethod,
                                                      minimalRecordState, recordFromPut)

            return recordFromPut

        except Exception as e:
            raise Exception("An error occurred while updating state.") from e

    def Delete(self, recordType, minimalRecordState):

        # It looks like a delete is simply setting some value to nothing
        # Once deleted, a record for the deleted element will be returned
        # This slightly changes things from the Set() function of this class
        # Here, our delete function will delete the record and then ensure
        # that the deleted record matches the url supplied

        try:
            nameOrId, nameOrIdValue = ApiStateEnforcer._GetNameOrIdFromRecord(minimalRecordState)
            nameOrIdForUrl = ApiStateEnforcer._FormatNameOrIdForApiUrl(nameOrId, nameOrIdValue)
            endpointSuffix = ApiStateEnforcer._GetApiUrlSuffixForRecordType(recordType)
            deleteUrl = "/api/{0}/{1}".format(endpointSuffix, nameOrIdForUrl)
            httpMethod = "DELETE"

            record = self.apiWrapper.MakeApiCall(deleteUrl, httpMethod, minimalRecordState, None)

            # When a record is created/updated, the record is returned as the result of the api call
            # We will need to verify that the record being returned corresponds to the record in question

            # In the case of the delete, the name/id is stored as the suffix in the url
            nameOrId = deleteUrl.split("/")[-1]
            recordMatch = ApiStateEnforcer._ConfirmModifiedRecordIdentity(nameOrIdValue, record)

            if not recordMatch:
                raise ModifiedRecordMismatchException(self.ModifiedRecordMismatchMessage, deleteUrl, httpMethod, minimalRecordState, record)

            return record

        except Exception as e:
            raise Exception("An error occurred while deleting state.") from e

    def EnsureState(self, recordType, desiredState, minimalRecordState):

        try:
            if desiredState.lower() not in ["present", "absent"]:
                raise Exception("The specified desired state '{0}' was not valid.".format(desiredState))

            # Get the current state
            # If the api throws a 404, the record does not exist
            # Otherwise it does exist
            actualRecordState = None
            try:
                actualRecordState = self.Check(recordType, minimalRecordState)
            except ForemanApiCallException as e:
                if e.results.status_code == 404:
                    pass

            # Determine what change is required (if any)
            if desiredState.lower() == "present":
                if not actualRecordState:
                    reason = self.MissingRecordMessage
                    changeRequired = True
                else:
                    statesMatch = self.Compare(minimalRecordState, actualRecordState)
                    changeRequired = not  statesMatch
                    reason = self.StateMismatchMessage
            if desiredState.lower() == "absent":
                if not actualRecordState:
                    changeRequired = False
                    reason = self.RecordAlreadyAbsentMessage
                else:
                    reason = self.ExtraRecordMessage
                    changeRequired = True

            # If not change is required, our work is done
            if not changeRequired:
                return { "changed": False, "reason": reason}

            # Do the change
            modifiedRecord = None
            if reason == self.MissingRecordMessage:
                modifiedRecord = self.Set(recordType, minimalRecordState)
            elif reason == self.ExtraRecordMessage:
                modifiedRecord = self.Delete(recordType, minimalRecordState)
            elif reason == self.StateMismatchMessage:
                # Do the update rather than a delete / set
                # modifiedRecord = self.Delete(recordType, minimalRecordState)
                # modifiedRecord = self.Set(recordType, minimalRecordState)
                modifiedRecord = self.Update(recordType, minimalRecordState)

            # Return the results
            return {
                "changed" : changeRequired,
                "modifiedRecord" : modifiedRecord,
                "reason": reason
            }

        except Exception as e:
            raise Exception("An error occurred while ensuring the api state.") from e

