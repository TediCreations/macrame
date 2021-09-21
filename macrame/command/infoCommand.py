#!/usr/bin/env python

"""
Info command
"""

import os
from ..core.cli import Command
from ..core.utils import listPortNames


class InfoCommand(Command):
	"""
	Shows project specific information
	"""

	def run(self, args):
		"""
		Runs the command
		"""
		cwd = self.getArgument("directory")
		project_name = os.path.basename(os.path.normpath(cwd))
		ports = listPortNames()

		txt = f"Project: {project_name}\n"
		txt += f"Ports:   {ports}\n"
		print(txt)

		return 0
