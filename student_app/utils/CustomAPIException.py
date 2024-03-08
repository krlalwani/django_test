import traceback

class CustomAPIException(Exception):
    def __init__(self, message= None, status_code=500, exception= None):
        self.message = message
        self.status_code = status_code
        self.exception = exception
        # traceback.print.exc()