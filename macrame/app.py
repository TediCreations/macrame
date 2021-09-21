#!/usr/bin/env python

"""
App for launching macrame
"""

import sys
from .command.parser import MyParser
from .command.buildCommand import BuildCommand
from .command.runCommand import RunCommand
from .command.cleanCommand import CleanCommand
from .command.infoCommand import InfoCommand
from .command.toolCommand import ToolCommand
from .command.todoCommand import TodoCommand
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
		ToolCommand("tool", "Checks for tools")
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
