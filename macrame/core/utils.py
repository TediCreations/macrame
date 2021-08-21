#!/usr/bin/env python

import subprocess
import os


def run_command(cmd):
	"""
	Run a shell command
	"""

	rv = subprocess.call(cmd, shell=True)
	return rv


def listPortNames():
	"""
	Returns the available port names in the project.

	Ports are directories inside the 'root/port/' directory (if available).
	Port names are the name of those directories.

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
