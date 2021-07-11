#!/usr/bin/env python

import os
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

	def __init__(self):
		"""
		Initialization
		"""
		# Select makefile
		self.makefilePath = "Makefile"
		# self.makefilePath = getAbsResoursePath("Makefile")

	def build(self):
		"""
		Build the project
		"""
		# List ports
		ports = self._listPorts()

		if ports is None:
			print("No ports available!")
			rv = 1
		elif len(ports) == 0:
			print("Ports directory is empty!")
			rv = run_command(f"make -f {self.makefilePath}")
			return 0
		else:
			rv = run_command(f"make -f {self.makefilePath} PORT_NAME={ports[0]}")

		return rv

	def clean(self):
		"""
		Cleans the project's generated files
		"""
		rv = run_command(f"make -f {self.makefilePath} clean")
		return rv

	def _listPorts(self):
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
