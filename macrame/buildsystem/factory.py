#!/usr/bin/env python

"""
???
"""

from ..core.exceptions import UserInputError
from .makefile import MakefileBuildManager


class BuildFactory:
	"""
	Manages the way that the build system is called
	"""

	def __init__(self, project_path, port_name, force_remote):
		"""
		Initialization
		"""

		self.build_manager = None

		if MakefileBuildManager.is_project_usable(project_path):
			self.build_manager = MakefileBuildManager(
				project_path=project_path, port_name=port_name, use_local_makefile=not force_remote,
			)
		else:
			raise UserInputError("Could not build the project")

	def get_manager(self):
		return self.build_manager
