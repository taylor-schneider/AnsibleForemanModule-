import json

class ModuleArgumentParser():

    @staticmethod
    def ParseModuleArguments(stdinJsonString):

        try:
            # The purpose of this function is to examine the arguments and
            # Extract the following pieces of information:
            #       Record Type
            #       Desired State

            # The first thing to do is get the record type
            # This is dynamic and could be anything
            # We will have to check the argument keys against a blacklist

            knownParameterNames = ["apiUrl", "username", "password", "verifySsl", "state"]
            stdinJsonDict = json.loads(stdinJsonString)
            possibleRecordTypes = []
            for key, value in stdinJsonDict['ANSIBLE_MODULE_ARGS'].items():
                if not key.startswith("_") and not key in knownParameterNames:
                    possibleRecordTypes.append(key)

            if len(possibleRecordTypes) is not 1:
                raise Exception("The foreman record type could not be determined.")

            recordType = possibleRecordTypes[0]

            # Once we know the record type we can determine the desired state
            record = stdinJsonDict['ANSIBLE_MODULE_ARGS'][recordType]

            if "state" not in record.keys():
                raise Exception("The record object supplied in the playbook did not contain the required 'state' field.")

            desiredState = record["state"]

            # After that we can remove the state key from the record
            # The field was for the ansible module and is not recognized by
            # foreman's api

            record.pop("state", None)

            return recordType, desiredState, record

        except Exception as e:
            raise Exception("An error occurred while parsing ") from e