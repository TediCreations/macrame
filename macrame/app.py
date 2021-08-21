#!/usr/bin/env python

from .commands import MyParser
from .commands import build_Command
from .commands import clean_Command
from .commands import info_Command
from .test import test_Command


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
		info_Command("info", "shows project specific information")
		test_Command("test", "this is a test")

	def run(self):
		return self.parser.handle()


def app_run():
	app = App()
	rv = app.run()
	exit(rv)


if __name__ == '__main__':
	app_run()
