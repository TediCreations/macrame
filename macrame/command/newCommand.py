#!/usr/bin/env python

"""New command."""

import os
from ..core.cli import Command
from ..resource import get_abs_resourse_path
from ..core.utils import copytree


class NewCommand(Command):
	"""Instantiates a new macrame project."""

	def run(self, args):
		"""
		Runs the command.

		args: The command arguments.
		"""
		rv = 0

		source_dir = get_abs_resourse_path("new_project")
		destination_dir = os.path.abspath(args.directory)

		# Getting the list of directories
		listDir = os.listdir(destination_dir)
		listDir = [x for x in listDir if not x.startswith('.')]

		if len(listDir):
			self.error("Directory is Not empty")

		try:
			copytree(source_dir, destination_dir)
		except KeyboardInterrupt:
			for item in listDir:
				os.remove(item)
			self.error()

		return rv
