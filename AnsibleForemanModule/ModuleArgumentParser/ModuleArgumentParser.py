

class ModuleArgumentParser():

    @staticmethod
    def ParseModuleArguments(moduleArguments):

        # The purpose of this function is to examine the arguments and
        # Extract the following pieces of information:
        #       Record Type
        #       Record
        #       Desired State

         foremanRecordStateObject = moduleArguments["desiredRecordState"]

        #if "state" not in desiredRecordState.keys():
        #    raise Exceptions("The module arguments supplied did not contain the ")


