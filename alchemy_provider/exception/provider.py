"""
Implements exception for alchemy provider
"""
from .base import BaseProviderException


class ObjectDoesNotExistException(BaseProviderException):
    detail = 'Object does not exist'


class FiltersMustBePassedException(BaseProviderException):
    detail = 'Filters must be passed'


class AttributeMustBeSetException(BaseProviderException):
    detail = 'Attribute must be set'


class ColumnDoesNotExistException(BaseProviderException):
    detail = 'Column does not exist'


class LookupOperatorNotFoundException(BaseProviderException):
    detail = 'Lookup operator not found'


class ColumnIsUniqueException(BaseProviderException):
    detail = 'Column is unique'


class IncorrectReferenceNameException(BaseProviderException):
    detail = 'Incorrect reference name'
