class DeletedRecordMismatchException(Exception):

    def __init__(self, message, deleteUrl, deletedRecord):

        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        self.deleteUrl = deleteUrl
        self.deletedRecord = deletedRecord