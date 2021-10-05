#!/usr/bin/env python

"""Build System Factory."""

from ..core.exceptions import UserInputError
from .adt import BuildManager
from .makefile import MakefileBuildManager


class BuildFactory:  # pylint: disable=R0903
	"""Factory that creates the build system automatically."""

	def __init__(self, project_path, port_name, force_remote) -> None:
		"""
		Initialization of the build factory.

		param: project_path The root directory of the project.
		param: port_name The name of the port.
		param: force_remote True to select static makefile. False to select local makefile.
		"""

		self.build_manager = None

		if MakefileBuildManager.is_project_usable(project_path):
			self.build_manager = MakefileBuildManager(
				project_path=project_path, port_name=port_name, use_local_makefile=not force_remote,
			)
		else:
			raise UserInputError("Could not build the project")

	def get_manager(self) -> BuildManager:
		"""Returns the build manager."""
		return self.build_manager
