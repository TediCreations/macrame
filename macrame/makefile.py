#!/usr/bin/env python

"""
Make and makefile manager
"""

import os
from .core.exceptions import UserInputError
from .core.utils import run_command
from .core.utils import listPortNames


def is_makefile_exist():
	"""
	Checks is a local Makefile exists in the current working directory
	"""
	rv = False
	if os.path.isfile("Makefile"):
		rv = True

	return rv


def get_abs_resourse_path(rel_resourse_path):
	"""
	Get the absolute path of a resourse.

	Resourse is a file located in the static directory.
	"""

	resourse_py_path = os.path.dirname(os.path.abspath(__file__))
	root_path = os.path.abspath(os.path.join(resourse_py_path, "../static"))
	abs_resourse_path = os.path.join(root_path, rel_resourse_path)
	return abs_resourse_path


class BuildManager:
	"""
	Manages the way that Make is called
	"""

	def __init__(self, port_name=None, use_local_makefile=True):
		"""
		Initialization

		param: port_name   The name of the port.
		param: use_local_makefile   True to select local makefile. False to select static makefile.
		"""
		# Select makefile
		if port_name == "":
			self.port_name = None
		else:
			self.port_name = port_name

		# Decide upon local or remote makefile
		self.makefile_path = get_abs_resourse_path("Makefile")
		if is_makefile_exist() is True and use_local_makefile is True:
			self.makefile_path = "Makefile"

		# List ports
		self.ports = listPortNames()

		# Validation
		if self.port_name is not None and self.ports is None:
			raise UserInputError(f"Port name '{self.port_name}' is not available")

	def build(self):
		"""
		Builds the project
		"""
		cmd = None
		if self.ports is None:
			cmd = f"make -f {self.makefile_path}"
		elif self.port_name is None and self.ports is not None:
			cmd = f"make -f {self.makefile_path} PORT_NAME={self.ports[0]}"
		elif self.port_name in self.ports:
			cmd = f"make -f {self.makefile_path} PORT_NAME={self.port_name}"
		else:
			raise UserInputError(f"Port name '{self.port_name}' was not found in available ports")

		rv = run_command(cmd)

		return rv

	def clean(self):
		"""
		Cleans the project's generated files
		"""
		rv = run_command(f"make -f {self.makefile_path} clean")
		return rv

	def run(self):
		"""
		Executes the program under development
		"""
		cmd = None
		if self.ports is None:
			cmd = f"make -f {self.makefile_path} run"
		elif self.port_name is None and self.ports is not None:
			cmd = f"make -f {self.makefile_path} PORT_NAME={self.ports[0]} run"
		elif self.port_name in self.ports:
			cmd = f"make -f {self.makefile_path} PORT_NAME={self.port_name} run"
		else:
			raise UserInputError(f"Port name '{self.port_name}' was not found in available ports")

		rv = run_command(cmd)

		return rv
