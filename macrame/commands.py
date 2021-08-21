#!/usr/bin/env python

import os
from .cli import Parser
from .cli import Command
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

		cwdPath = os.path.abspath(os.getcwd())
		self.parser.add_argument(
			'-C', '--directory',
			default=cwdPath,
			help="changes current working directory")
		self.parser.add_argument(
			'-v', '--version',
			action='store_true',
			help="output version and exit")

	def logic(self, args):
		"""
		Configuration of arguments
		"""
		# Version information
		if args.version:
			print(f"Version: {__version__}")
			exit(0)

		# Working directory
		directory = os.path.abspath(args.directory)
		if not os.path.isdir(directory):
			self.error(f"The directory {directory} does not exist!")
		os.chdir(directory)


class build_Command(Command):
	"""
	Builds the software
	"""

	def config(self):
		"""
		Configuration of arguments
		"""
		"""
		self.subparser.add_argument(
			'-V', '--verbose',
			action='store_true',
			help='show extra information')
		"""
		# Port name
		self.subparser.add_argument(
			'-p', '--port',
			default="",
			type=str,
			help="the port name.")
		pass

	def run(self, args):
		"""
		Runs the command
		"""

		buildManager = BuildManager(
			portName=args.port
		)
		rv = buildManager.build()
		return rv


class clean_Command(Command):
	"""
	Removes generated files
	"""

	def run(self, args):
		"""
		Runs the command
		"""

		buildManager = BuildManager()
		rv = buildManager.clean()
		return rv
