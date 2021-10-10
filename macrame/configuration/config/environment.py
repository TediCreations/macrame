#!/usr/bin/env python

"""Environment config."""

import os
import ast
from ..adt import Config
from ..exceptions import NotValidConfiguration
from ..exceptions import InvalidAttribute
from ..exceptions import OperationOnIncompatibleConfigs


class Environment(Config):
	# pylint: disable=no-member

	"""Configuration class for ennvironment variables."""

	available_methods = [None, "append"]

	def get_label(self) -> str:
		"""Return the label(name) of the config."""

		return self.name

	def get_mandatory_atrributes_list(self) -> list:
		"""Return the mandatory attributes"""

		attribute_list = [
			"name",
			"value"
		]

		return attribute_list

	def get_optional_atrributes_list(self) -> list:
		"""Return the optional attributes."""

		attribute_list = [
			"condition",
			"method",
			"description"
		]

		return attribute_list

	def rule_checks(self) -> None:
		"""Perform custom tests at init."""

		if self.method not in self.available_methods:
			print(f"self.method: {self.method}")
			raise InvalidAttribute(self, "method")

	# TODO: Continue with features (condition)
	def __add__(self, other):
		"""
		Adds self with an other environment objects.

		param: other The Environment object to add with.
		"""

		# Test if merge is possible
		if self.name != other.name:
			raise OperationOnIncompatibleConfigs(
				f"Trying to add '{self.name}' + '{other.name}' environment variables"
			)

		new_dict = {
			"condition": "True",
			"name": self.name,
			"value": None,
			"description": None,
			"method": None
		}

		# Test other
		if other.method == "append":
			new_dict["value"] = self.value + " " + other.value
		else:
			new_dict["value"] = other.value

		new_dict["method"] = other.method

		environment_obj = Environment(new_dict)

		return environment_obj

	def register(self) -> None:
		"""Registers the environment variable."""

		condition_result = True
		if self.condition:
			condition = self.condition
			condition = self._parse_env_variables(condition)

			try:
				condition_result = ast.literal_eval(condition)
			except (NameError, SyntaxError) as e:
				raise NotValidConfiguration(
					"Invalid syntax in Environment variable condition: ({self.condition})"
				) from e

		if condition_result:
			value = self._parse_env_variables(self.value)
			new_value = value

			if self.method == "append":
				old_value = os.environ.get(self.name)
				if old_value:
					new_value = os.environ[self.name] + " " + new_value

			os.environ[self.name] = new_value
