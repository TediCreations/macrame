#!/usr/bin/env python

"""Abstract data types for configurations."""

import os
import re
from abc import ABC
from abc import abstractmethod
# from ..core.utils import typify_string
from ..core.colors import Color
from .exceptions import MandatoryConfigAttributeMissing


class Config(ABC):

	"""Base class for all configurations."""

	def __init__(self, config) -> None:
		"""
		Initialize tools config.

		params config: Dictionary that holds the tool configuration
		"""

		# Validate configuration
		if not isinstance(config, dict):
			raise TypeError(f"Not a valid '{self.__class__.__name__}' configuration")

		# Automatically load dictionary keys as members
		for key, value in config.items():
			# TODO: Use typify_strings
			#
			# typified_value = typify_string(value)
			# print(f"Setting: {key}: {value} | {typified_value}")
			#
			setattr(self, key, value)

		# Verify mandatory config attributes
		mandatory_attribute_list = self.get_mandatory_atrributes_list()
		if mandatory_attribute_list is not None:
			for mandatory_attribute in mandatory_attribute_list:
				self._verify_mandatory_attribute(mandatory_attribute)

		# Verify optional config attributes
		optional_attribute_list = self.get_optional_atrributes_list()
		if optional_attribute_list is not None:
			for optional_attribute in optional_attribute_list:
				self._verify_optional_attribute_or_none(optional_attribute)

		# Check rules
		self.rule_checks()

	def __str__(self):
		"""Get string that represents the object."""

		txt = f"[{Color.BLUE}{self.__class__.__name__}{Color.RESET}]\n"
		for key, value in self.__dict__.items():
			txt += f"{key}: {Color.YELLOW}{value}{Color.RESET}\n"

		return txt

	@abstractmethod
	def get_label(self) -> str:
		"""Return the label(name) of the config"""

	@abstractmethod
	def get_mandatory_atrributes_list(self) -> list:
		"""Return the mandatory attributes."""

	@abstractmethod
	def get_optional_atrributes_list(self) -> list:
		"""Return the optional attributes."""

	@abstractmethod
	def rule_checks(self) -> None:
		"""Perform custom tests at init."""

	def _verify_mandatory_attribute(self, attribute_string: str):
		"""
		Set an attribute given the string representation.

		attribute_string: The atribute string representation
		"""
		try:
			getattr(self, attribute_string)
		except AttributeError as e:
			raise MandatoryConfigAttributeMissing(self, attribute_string) from e

	def _verify_optional_attribute_or_none(self, attribute_string: str):
		"""
		Given a an optional attribute string representation,
		assign it into None if it is not provided
		or the actual value.

		attribute_string: The attribute string representation
		"""
		value = None
		try:
			value = getattr(self, attribute_string)
		except AttributeError:
			value = None

		setattr(self, attribute_string, value)

	# TODO: Refactor the use of this function
	@classmethod
	def _parse_env_variables(cls, test_str: str) -> str:
		"""
		Parses an environmental variable in the config
		and returns the match.

		param: test_str The string to apply the regular expression to.
		"""

		reply = test_str

		regex = r"(?:\$\{)(.*)(?:\})"  # {}
		# regex = r"(?:\$\()(.*)(?:\))"  # ()
		matches = re.finditer(regex, test_str, re.MULTILINE)

		for _, match in enumerate(matches, start=1):
			# Find env variable
			match_str = match.group(1)
			value_str = os.getenv(match_str)
			if value_str is None:
				value_str = ""

			# Replace
			# Beware that curly braces below are escaped
			reply = reply.replace(f"${'{'}{match_str}{'}'}", value_str)

		return reply
