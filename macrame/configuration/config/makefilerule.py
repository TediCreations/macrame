#!/usr/bin/env python

"""Makefile rule config."""

from ..adt import Config


class MakefileRule(Config):
	# pylint: disable=no-member

	"""
	Configuration class for a Makefile rule.

	targets: prerequisites
		commands
	"""

	def get_label(self) -> str:
		"""Return the label(name) of the config"""

		return self.targets

	def get_mandatory_atrributes_list(self) -> list:
		"""Return the mandatory attributes."""

		attribute_list = [
			"targets",
			"prerequisites"
		]

		return attribute_list

	def get_optional_atrributes_list(self) -> list:
		"""Return the optional attributes."""

		attribute_list = [
			"command",
			"description"
		]

		return attribute_list

	def rule_checks(self) -> None:
		"""Perform custom tests at init."""

	def generate_rule(self) -> None:
		"""Do the config."""
		# project_dirpath = "XXX"
		# print(f"Project: {project_dirpath}")

		txt = ""
		if self.phony:
			txt += f"PHONY: {self.targets}\n"
		txt += f"{self.targets}:"
		if self.prerequisites:
			txt += f" {self.prerequisites}\n"
		else:
			txt += "\n"
		if self.command:
			stripped_command = self.command.rstrip()
			txt += f"{stripped_command}\n"
		else:
			txt += ":\n"
		txt += "\n"

		return txt
