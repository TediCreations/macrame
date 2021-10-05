#!/usr/bin/env python

"""Abstract data types for building system."""

from abc import ABC
from abc import abstractmethod


class ConfigLoader(ABC):  # pylint: disable=R0903
	"""Abstract data type for loading the config."""

	@abstractmethod
	def get(self) -> list:
		"""Get the list of configs."""


class ConfigProcessor(ABC):  # pylint: disable=R0903
	"""Abstract data type for processing the config."""

	@abstractmethod
	def handle(self) -> None:
		"""Applies the config."""


class BuildManager(ABC):
	"""Abstract for managing the builds."""

	@staticmethod
	@abstractmethod
	def is_project_usable(project_path) -> bool:
		"""
		Checks is the project meets the standards
		to use this build manager.

		param: project_path The absolute path of the project
		"""

	@abstractmethod
	def build(self) -> None:
		"""
		Builds the project
		"""

	@abstractmethod
	def clean(self) -> None:
		"""Cleans the project's generated files."""

	@abstractmethod
	def run(self) -> None:
		"""Executes the program under development."""
