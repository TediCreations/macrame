#!/usr/bin/env python

"""
Clean command
"""

from ..core.cli import Command
from ..makefile import MakefileBuildManager


class CleanCommand(Command):
	"""
	Removes generated files
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

	def run(self, args):
		"""
		Runs the command
		"""
		build_manager = MakefileBuildManager(use_local_makefile=not args.force_remote)
		rv = build_manager.clean()

		return rv
