#!/usr/bin/env python

"""
Build command
"""

from ..core.cli import Command
from ..core.utils import listPortNames
from ..makefile import MakefileBuildManager


class BuildCommand(Command):
	"""
	Builds the software
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
		build_manager = MakefileBuildManager(
			port_name=args.port,
			use_local_makefile=not args.force_remote
		)
		rv = build_manager.build()

		return rv
