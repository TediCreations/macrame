#!/usr/bin/env python

"""Tool config."""

from ...core.version import Version
from ...core.utils import run_command2
from ...core.utils import acquireCliProgramVersion
from ...core.utils import which
from ..adt import Config


class Tool(Config):
	# pylint: disable=no-member

	"""
	Configuration class for Tools.
	"""

	def get_label(self) -> str:
		"""Return the label(name) of the config."""
		return self.name

	def get_mandatory_atrributes_list(self) -> list:
		"""Return the mandatory attributes."""

		attribute_list = [
			"name"
		]

		return attribute_list

	def get_optional_atrributes_list(self) -> list:
		"""Return the optional attributes."""

		attribute_list = [
			"arg",
			"compare",
			"version"
		]

		return attribute_list

	def rule_checks(self) -> None:
		"""Perform custom tests at init."""

	def __add__(self, other):
		# TODO: Add properly
		return self

	def check(self) -> None:
		"""
		Checks a tools existance in the system
		and its version.
		"""
		# Check existance
		is_available = which(self.name)
		if is_available is None:
			raise Exception(f"{self.name} not found!")

		# Check version
		cmd = self.name + " " + self.arg

		raw_version_string = str(run_command2(cmd))
		parsed_version_string = acquireCliProgramVersion(raw_version_string)

		actual_version = Version(parsed_version_string)
		desired_version = Version(self.version)

		result = False
		if self.compare == "==":
			result = actual_version == desired_version
		elif self.compare == ">=":
			result = actual_version >= desired_version
		elif self.compare == ">":
			result = actual_version > desired_version
		elif self.compare == "<=":
			result = actual_version <= desired_version
		elif self.compare == "<":
			result = actual_version < desired_version

		if result is False:
			raise Exception(f"{self.name} is not {self.compare} {self.version}")
