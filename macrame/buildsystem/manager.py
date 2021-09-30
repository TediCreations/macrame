#!/usr/bin/env python

"""
???
"""

from abc import ABC
from abc import abstractmethod


class BuildManager(ABC):
	"""
	Abstract for managing the builds
	"""

	@staticmethod
	@abstractmethod
	def is_project_usable(project_path) -> bool:
		"""
		Checks is the project meets the standards
		to use this build manager

		param: project_path The absolute path of the project
		"""

	@abstractmethod
	def build(self):
		"""
		Builds the project
		"""

	@abstractmethod
	def clean(self):
		"""
		Cleans the project's generated files
		"""

	@abstractmethod
	def run(self):
		"""
		Executes the program under development
		"""
