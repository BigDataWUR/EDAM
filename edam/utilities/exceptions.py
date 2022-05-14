class Error(Exception):
    """Base class for other exceptions"""
    pass


class TemplateDoesNotExist(Error):
    """Raised when template does not exist"""
    pass


class MetadataFileDoesNotExist(Error):
    """Raised when template does not exist"""
    pass


class ErrorWithTemplate(Error):
    """Raised when template does not exist"""
    pass


class FileDoesNotExist(Error):
    """Raised when file does not exist"""
    pass


class InputParameterDoesNotExist(Error):
    """Raised when InputParameter does not exist"""
    pass


class UrlInputParameterDoesNotExist(Error):
    """Raised when UrlInputParameter does not exist"""
    pass


class TemplateInputHeaderMismatch(Error):
    """Raised when Template and Input file headers do not match each other"""
    pass


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv
