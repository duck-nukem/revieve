class InputTransformerException(Exception):
    pass


class InvalidInputFileException(InputTransformerException):
    pass


class InvalidRowConfigurationException(InputTransformerException):
    pass
