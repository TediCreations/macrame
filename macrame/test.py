#!/usr/bin/env python

"""
Temporary test code
"""

import argparse
from buildutil.configParser import ConfigParser
from buildutil.configParser import array2Dict
from .core.cli import Command
from .core.version import Version
from .core.utils import run_command2
from .core.utils import acquireCliProgramVersion


class TestCommand(Command):
	"""
	Test Command
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
		print(f"File: '{args.file}'")

		version_list = [
			["doesnotexist", "--version", "==", ""],
			["make", "--version", "==", "4.1"],
			["gcc", "--version", "==", "7.5"],
			["arm-none-eabi-gcc", "--version", "==", "10.2.1"],
			["g++", "--version", "==", "7.5"],
			["git", "--version", "==", "2.17.1"],
			["ls", "--version", ">=", "8.28"],
			["python -m macrame", "--version", "==", "2.1"],
			["python", "--version", "==", "3.9"]
		]

		for version in version_list:
			program = version[0]
			args = version[1]
			comparison = version[2]
			string_with_desired_version = version[3]
			cmd = program + " " + args

			string_with_actual_version = str(run_command2(cmd))

			string_with_actual_version = acquireCliProgramVersion(string_with_actual_version)

			try:
				actual_version = Version(string_with_actual_version)
			except Exception:
				print(f"'{program}' is not available")
				continue
			desired_version = Version(string_with_desired_version)

			result = None
			if comparison == "==":
				result = actual_version == desired_version
			elif comparison == ">=":
				result = actual_version >= desired_version
			elif comparison == ">":
				result = actual_version > desired_version
			elif comparison == "<=":
				result = actual_version <= desired_version
			elif comparison == "<":
				result = actual_version < desired_version

			print(f"{program:18} | {actual_version}\t{comparison:2} {desired_version}\t| {result}")

		lst = array2Dict([
			# Section Key Default Options
			["MAKE", "PORT", "posix", {"posix", "stm32f072rb"}],
			["MAKE", "TARGET", "dbg", {"dbg", "rel"}],
			["MAKE", "test", "dbg", {"dbg", "rel"}],
		])

		ini_filepath = "setup.ini"
		parser = ConfigParser(ini_filepath, lst)
		parser.setenv()

		return 0
