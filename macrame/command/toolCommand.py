#!/usr/bin/env python

"""
Tool command
"""

import argparse
import toml
from ..core.cli import Command
from ..configuration.config import Tool


class ToolCommand(Command):
	"""
	Tool Command
	"""

	def config(self):
		"""
		Configuration of arguments

		"""
		self.subparser.add_argument(
			'-f',
			'--file',
			help='A readable file',
			# metavar='FILE',
			type=argparse.FileType('r'),
			default=None)

	def run(self, args):
		"""
		Runs the command
		"""

		if args.file is not None:
			print(f"File: '{args.file.name}'")
			parsed_toml = toml.load(args.file)

			# print(parsed_toml)

			for tool in parsed_toml['Tool']:
				# print(tool)
				t = Tool(tool)
				rv = t.check()
				print(t)
				print(f"Result: {rv}")
				print("")

		return 0
