#!/usr/bin/env python

"""Exceptions for configurations."""


class NotValidConfiguration(Exception):
	"""
	Exception for when a config is not valid.

	param: msg The message string to show when exception occurs.
	"""

	def __init__(self, msg: str) -> None:
		message = str(msg)
		super().__init__(message)


class MandatoryConfigAttributeMissing(Exception):
	"""
	Exception for when a config is missing a mandatory attribute.
	"""

	def __init__(self, config, attribute: str) -> None:
		message = f"'{config.__class__.__name__}' is missing mandatory attribute '{attribute}'"
		super().__init__(message)


class InvalidAttribute(Exception):
	"""
	Exception for when a config has an invalid attribute.
	"""

	def __init__(self, config, attribute: str) -> None:
		message = f"'{config.__class__.__name__}.{attribute}' is invalid"
		super().__init__(message)


class OperationOnIncompatibleConfigs(Exception):
	"""
	Exception for when a config can not handle an operation.

	param: msg The message string to show when exception occurs.
	"""

	def __init__(self, msg: str) -> None:
		message = str(msg)
		super().__init__(message)
