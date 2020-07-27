class Error(Exception):
    """Base class for other exceptions"""
    pass


class TemplateDoesNotExist(Error):
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
