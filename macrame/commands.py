#!/usr/bin/env python

"""
Parser and build commands
"""

import os
import sys
from .core.cli import Parser
from .core.cli import Command
from .core.utils import listPortNames
from .makefile import BuildManager
from . import __version__


class MyParser(Parser):
	"""
	Parser for the buildsystem
	"""

	def config(self):
		"""
		Configuration of arguments
		"""

		cwd_path = os.path.abspath(os.getcwd())
		self.parser.add_argument(
			'-C', '--directory',
			default=cwd_path,
			help="changes current working directory")
		self.parser.add_argument(
			'-v', '--version',
			action='store_true',
			help="output version and exit")

	def run(self, args):
		"""
		Configuration of arguments
		"""
		# Version information
		if args.version:
			print(f"Version: {__version__}")
			sys.exit(0)

		# Working directory
		directory = os.path.abspath(args.directory)
		if not os.path.isdir(directory):
			self.error(f"The directory {directory} does not exist!")
		os.chdir(directory)


class BuildCommand(Command):
	"""
	Builds the software
	"""

	def config(self):
		"""
		Configuration of arguments
		"""

		# self.subparser.add_argument(
		# 	'-V', '--verbose',
		# 	action='store_true',
		# 	help='show extra information')

		# Port name
		self.subparser.add_argument(
			'-p', '--port',
			default="",
			type=str,
			help="the port name.")

	def run(self, args):
		"""
		Runs the command
		"""
		build_manager = BuildManager(
			port_name=args.port
		)
		rv = build_manager.build()

		return rv


class CleanCommand(Command):
	"""
	Removes generated files
	"""

	def run(self, args):
		"""
		Runs the command
		"""
		build_manager = BuildManager()
		rv = build_manager.clean()

		return rv


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
