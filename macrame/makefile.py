#!/usr/bin/env python

import os
from .exceptions import UserInputError
from .utils import run_command


'''
def getAbsResoursePath(relResoursePath):
	"""
	Get the absolute path of a resourse.

	Resourse is a file located in the static directory.
	"""

	resoursePyPath = os.path.dirname(os.path.abspath(__file__))
	rootPath = os.path.abspath(os.path.join(resoursePyPath, "../static"))
	absResoursePath = os.path.join(rootPath, relResoursePath)
	return absResoursePath
'''


class BuildManager(object):
	"""
	Manages the way that Make is called
	"""

	def __init__(self, portName=None):
		"""
		Initialization

		param: portName   The name of the port.
		"""
		# Select makefile
		if portName == "":
			self.portName = None
		else:
			self.portName = portName
		self.makefilePath = "Makefile"
		# self.makefilePath = getAbsResoursePath("Makefile")

		# List ports
		self.ports = self._listPortNames()

		# Validation
		if self.portName is not None and self.ports is None:
			# 2
			raise UserInputError(f"Port name '{self.portName}' is not available")

	def build(self):
		"""
		Builds the project
		"""
		cmd = None
		if self.ports is None:
			cmd = f"make -f {self.makefilePath}"
		elif self.portName is None and self.ports is not None:
			cmd = f"make -f {self.makefilePath} PORT_NAME={self.ports[0]}"
		elif self.portName in self.ports:
			cmd = f"make -f {self.makefilePath} PORT_NAME={self.portName}"
		else:
			raise UserInputError(f"Port name '{self.portName}' was not found in available ports")

		rv = run_command(cmd)

		return rv

	def clean(self):
		"""
		Cleans the project's generated files
		"""
		rv = run_command(f"make -f {self.makefilePath} clean")
		return rv

	def _listPortNames(self):
		"""
		Returns the available port names in the project.

		Ports are directories in inside the 'root/port/' directory.
		Port names are the name of the directories.

		Returns:
		- list of port name strings (if available).
		- None if port dir is not available or if not any ports are available.
		"""
		rv = None
		portNameList = list()
		portPath = "port"
		if os.path.isdir(portPath):
			dirCandidateList = os.listdir(portPath)
			for dirCandidate in dirCandidateList:
				dirCandidatePath = os.path.join(portPath, dirCandidate)
				if os.path.isdir(dirCandidatePath):
					portNameList.append(dirCandidate)
			portNameList.sort()

		if len(portNameList) != 0:
			rv = portNameList

		return rv

	'''
	def listPorts(self):
		"""
		Returns the available ports in the project

		Returns:
		- list of strings with port names if available.
		- Empty string is not any ports available.
		- None if port dir is not available.
		"""
		portNameList = list()
		portPath = "port"
		if os.path.isdir(portPath):
			dirCandidateList = os.listdir(portPath)
			for dirCandidate in dirCandidateList:
				dirCandidatePath = os.path.join(portPath, dirCandidate)
				if os.path.isdir(dirCandidatePath):
					portNameList.append(dirCandidate)
			portNameList.sort()
		else:
			portNameList = None

		return portNameList
	'''
