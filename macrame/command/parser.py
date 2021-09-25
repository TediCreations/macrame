#!/usr/bin/env python

"""
Parser and build commands
"""

import io
import os
import sys
from ..core.complete import complete
from ..core.cli import Parser
from .. import __version__


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
			completion_file = os.path.join(filepath, f"../core/completion.{shell}")
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
