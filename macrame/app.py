#!/usr/bin/env python

from .cli import Command
from .commands import MyParser
from .commands import build_Command
from .commands import clean_Command
import argparse


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
		return 0


class App(object):
	"""
	Macrame application
	"""

	def __init__(self):
		"""
		Initialises the app
		"""

		self.parser = MyParser(
			"mac[rame]",
			"Utility to build Assembly/C/C++ projects",
			"Author: Kanelis Elias")
		build_Command("build", "builds the software")
		clean_Command("clean", "remove the generated files")
		test_Command("test", "this is a test")

	def run(self):
		return self.parser.run()


def app_run():
	app = App()
	rv = app.run()
	exit(rv)


if __name__ == '__main__':
	app_run()
