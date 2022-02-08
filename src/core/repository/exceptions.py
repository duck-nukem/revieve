class RepositoryException(Exception):
    pass


class UnsupportedDataSourceException(RepositoryException):
    pass


class ItemNotFoundException(RepositoryException):
    pass
