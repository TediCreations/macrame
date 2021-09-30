#!/usr/bin/env python

"""
Run command
"""

import os
from ..core.cli import Command
from ..core.utils import listPortNames
from ..buildsystem.factory import BuildFactory


class RunCommand(Command):
	"""
	Executes the program under development
	"""

	def config(self):
		"""
		Configuration of arguments
		"""

		# Local or remote makefile
		self.subparser.add_argument(
			'-r', '--force_remote',
			default=False,
			action='store_true',
			help="use the tools internal build system config files")

		# Port name
		self.subparser.add_argument(
			'-p', '--port',
			default="",
			choices=listPortNames(),
			type=str,
			help="the port name.")

	def run(self, args):
		"""
		Runs the command
		"""
		project_path = os.path.abspath(args.directory)

		build_factory = BuildFactory(project_path, args.port, args.force_remote)
		rv = build_factory.get_manager().run()

		return rv
