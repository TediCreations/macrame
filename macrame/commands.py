#!/usr/bin/env python

"""
Parser and build commands
"""

import os
import sys
from .core.cli import Parser
from .core.cli import Command
from .core.utils import listPortNames
from .core.utils import egrep
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

		# Local or remote makefile
		self.subparser.add_argument(
			'-r', '--remote',
			default=False,
			action='store_true',
			help="use the tools internal build system config files (excludes '--local')")
		self.subparser.add_argument(
			'-l', '--local',
			dest='remote',
			action='store_false',
			help="use the project's local build system config files (excludes '--remote')")

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
			port_name=args.port,
			use_local_makefile=not args.remote
		)
		rv = build_manager.build()

		return rv


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
			'-r', '--remote',
			default=False,
			action='store_true',
			help="use the tools internal build system config files (excludes '--local')")
		self.subparser.add_argument(
			'-l', '--local',
			dest='remote',
			action='store_false',
			help="use the project's local build system config files (excludes '--remote')")

	def run(self, args):
		"""
		Runs the command
		"""
		build_manager = BuildManager(use_local_makefile=not args.remote)
		rv = build_manager.clean()

		return rv


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
			'-r', '--remote',
			default=False,
			action='store_true',
			help="use the tools internal build system config files (excludes '--local')")
		self.subparser.add_argument(
			'-l', '--local',
			dest='remote',
			action='store_false',
			help="use the project's local build system config files (excludes '--remote')")

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
			port_name=args.port,
			use_local_makefile=not args.remote
		)
		rv = build_manager.run()

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


class TodoCommand(Command):
	"""
	Lists programmer's todos
	"""

	def config(self):
		"""
		Configuration of arguments
		"""

		# Whole words
		self.subparser.add_argument(
			'-w', '--whole_words',
			action='store_true',
			help="search only for whole words")
		# Keywords
		self.subparser.add_argument(
			'-k', '--keywords',
			default=['todo', 'bug', 'fix'],
			action='store',
			type=str,
			nargs='*',
			help="keywords to search in the project")

	def run(self, args):
		"""
		Runs the command
		"""
		keywords = args.keywords
		whole_words = args.whole_words

		rv = 0
		if len(keywords) == 0:
			self.error("Please select one or more keywords")
		else:
			for keyword in keywords:
				rv = egrep(keyword, whole_words=whole_words)

		return rv
