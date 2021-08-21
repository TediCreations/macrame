#!/usr/bin/env python

"""
Make and makefile manager
"""

from .core.exceptions import UserInputError
from .core.utils import run_command
from .core.utils import listPortNames


# def getAbsResoursePath(relResoursePath):
# 	"""
# 	Get the absolute path of a resourse.
#
# 	Resourse is a file located in the static directory.
# 	"""
#
# 	resoursePyPath = os.path.dirname(os.path.abspath(__file__))
# 	rootPath = os.path.abspath(os.path.join(resoursePyPath, "../static"))
# 	absResoursePath = os.path.join(rootPath, relResoursePath)
# 	return absResoursePath


class BuildManager:
	"""
	Manages the way that Make is called
	"""

	def __init__(self, port_name=None):
		"""
		Initialization

		param: port_name   The name of the port.
		"""
		# Select makefile
		if port_name == "":
			self.port_name = None
		else:
			self.port_name = port_name
		self.makefile_path = "Makefile"
		# self.makefile_path = getAbsResoursePath("Makefile")

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
