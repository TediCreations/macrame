#!/usr/bin/env python

import argparse
# import argcomplete
import os

_commandList = []
_parser = None
_subparser = None


class Parser(object):

	"""
	Supports the creation of commandline argument subcommands
	with support from argparse.
	"""

	def __init__(self, name, description, epilog):
		"""
		Creates an argument parser

		name: The name of the program
		description: Text explaining what the program does
		epilog: Text at the end of the help section
		"""

		global _parser
		if _parser is not None:
			raise Exception("Could not init parser")
		_parser = argparse.ArgumentParser(
			prog=name,
			description=description,
			epilog=epilog,
			fromfile_prefix_chars='@')

		global _subparser
		_subparser = _parser.add_subparsers(dest='cmd', description="")

		self.parser = _parser
		self.config()
		_parser = self.parser

	def error(self, message):
		"""
		Print error message and exit
		"""
		_parser.error(str(message))

	def config(self):
		"""
		Configuration of arguments

		Example

		self.parser.add_argument(
			'-v', '--version',
			action='store_true',
			help="get the version of the system")
		"""
		pass

	def run(self):
		# argcomplete.autocomplete(_parser)
		args = _parser.parse_args()
		subcommand = _parser.parse_args().cmd

		self.parser = _parser
		self.logic(args)
		# _parser = self.parser

		rv = 0
		global _commandList
		for command in _commandList:
			cmd_name = command['name']
			cmd_callback = command['callback']
			if cmd_name == subcommand:
				rv = cmd_callback(args)

		return rv

	def logic(self, args):
		pass


class Command(object):
	"""
	Supports the creation of commandline argument subcommands
	with support from argparse.
	"""

	def __init__(self, name, help=None):
		"""
		Creates an argument command

		parser: The argparse parser
		name: The name of the command
		help: Description of the command or None
		"""
		self.name = name
		global _parser
		if _parser is None:
			raise Exception(f"Could not append command '{self.name}' to the parser")

		global _subparser
		self.subparser = _subparser.add_parser(
			self.name,
			help=help)

		d = dict()
		d['name'] = self.name
		d['callback'] = self.run

		global _commandList
		_commandList.append(d)

		self.config()

	def error(self, message):
		"""
		Print error message and exit
		"""
		_parser.error(str(message))

	def config(self):
		"""
		Configuration of arguments
		"""
		# Example
		# self.subparser.add_argument(
		# 	'-v', '--version',
		# 	action='store_true',
		# 	help=f"get the version of the {self.name} system")
		pass

	def run(self, args):
		"""
		Configuration of arguments
		"""
		print(f"Command '{self.name}' just run!")
		return 0

	def check_directory(self, directoryPath):
		"""
		Check if this is a valid directory
		else exit with a message.
		"""
		if not os.path.isdir(directoryPath):
			self.error(f"The directory {directoryPath} does not exist!")
