#!/usr/bin/env python

from .core.cli import Command
import argparse

from buildutil.configParser import ConfigParser
from buildutil.configParser import array2Dict


class test_Command(Command):
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

		lst = array2Dict([
			# Section Key Default Options
			["MAKE", "PORT", "posix", {"posix", "stm32f072rb"}],
			["MAKE", "TARGET", "dbg", {"dbg", "rel"}],
			["MAKE", "test", "dbg", {"dbg", "rel"}],
		])

		iniFilepath = "setup.ini"
		parser = ConfigParser(iniFilepath, lst)
		parser.setenv()

		return 0
