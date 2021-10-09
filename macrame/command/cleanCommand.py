#!/usr/bin/env python

"""Clean command."""

import os
from ..core.cli import Command
from ..buildsystem.factory import BuildFactory


class CleanCommand(Command):
	"""Removes generated files."""

	def config(self):
		"""Configuration of arguments."""

		# Local or remote makefile
		self.subparser.add_argument(
			"-r", "--force_remote",
			default=False,
			action="store_true",
			help="use the tools internal build system config files",
		)

	def run(self, args):
		"""
		Runs the command.

		args: The command arguments.
		"""
		project_path = os.path.abspath(args.directory)

		build_factory = BuildFactory(project_path, None, args.force_remote)
		rv = build_factory.get_manager().clean()

		return rv
