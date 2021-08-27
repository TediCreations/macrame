#!/usr/bin/env python

"""
App for launching macrame
"""

import sys
from .commands import MyParser
from .commands import BuildCommand
from .commands import RunCommand
from .commands import CleanCommand
from .commands import InfoCommand
from .commands import TodoCommand
from .test import TestCommand


class App:
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
		BuildCommand("build", "builds the software")
		CleanCommand("clean", "remove the generated files")
		RunCommand("run", "executes the program")
		InfoCommand("info", "shows project specific information")
		TodoCommand("todo", "Lists programmer's todo/bug/fix keywords")
		TestCommand("test", "this is a test")

	def run(self):
		"""
		Runs the app
		"""
		return self.parser.handle()


def app_run():
	"""
	Convenient function to run the app
	"""

	app = App()
	rv = app.run()
	sys.exit(rv)


if __name__ == '__main__':
	app_run()
