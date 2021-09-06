#!/usr/bin/env python

"""
Parser and build commands
"""

import io
import os
import sys
from .core.complete import complete
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
		self.parser.add_argument(
			'--complete',
			help="Completion for shell")
		self.parser.add_argument(
			'--print_shell_completion_script',
			choices=["bash", "zsh"],
			help="Prints the script to be sources for shell completion")

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

		# Shell completion
		shell = args.print_shell_completion_script
		if shell:
			filepath = os.path.dirname(os.path.abspath(__file__))
			completion_file = os.path.join(filepath, f"./core/completion.{shell}")
			with io.open(completion_file, 'r', encoding='utf8') as completion_script:

				lines = completion_script.readlines()
				for line in lines:
					print(line.strip())
				completion_script.close()
				sys.exit(0)
		elif args.complete is not None:
			program_names = sorted(['mac', 'macrame'], key=len, reverse=True)

			raw = args.complete.strip(' ')
			raw = raw.rstrip(" -")

			for program_name in program_names:
				if raw.startswith(program_name):
					raw = raw[len(program_name):]
					raw = raw.lstrip(" ")
					break
			cli_args = raw

			rv = complete(self.parser, cli_args)
			print(rv)
			sys.exit(0)


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
		build_manager = BuildManager(
			port_name=args.port,
			use_local_makefile=not args.force_remote
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
			'-r', '--force_remote',
			default=False,
			action='store_true',
			help="use the tools internal build system config files")

	def run(self, args):
		"""
		Runs the command
		"""
		build_manager = BuildManager(use_local_makefile=not args.force_remote)
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
		build_manager = BuildManager(
			port_name=args.port,
			use_local_makefile=not args.force_remote
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
			choices=['todo', 'bug', 'fix'],
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
