#!/usr/bin/env python

import subprocess
import os
import sys
import re
import ast
import shutil
from typing import Optional


def which(program: str) -> Optional[str]:
	"""
	Alternative to UNIX which.

	param: program The program name or path.
	"""

	def is_exe(fpath):
		return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

	fpath, fname = os.path.split(program)
	if fpath:
		if is_exe(program):
			return program
	else:
		for path in os.environ["PATH"].split(os.pathsep):
			exe_file = os.path.join(path, program)
			if is_exe(exe_file):
				return exe_file

	return None


def copytree(src: str, dst: str, symlinks=False, ignore=None) -> None:
	"""
	Copy a file or all the contents of a directory.

	param: src The source file or directory
	param: dst The source file or directory
	param: symlinks Do you want symlinks to be copied
	param: ignore What files to ignore
	"""

	for item in os.listdir(src):
		s = os.path.join(src, item)
		d = os.path.join(dst, item)
		if os.path.isdir(s):
			shutil.copytree(s, d, symlinks, ignore)
		else:
			shutil.copy2(s, d)


def acquireCliProgramVersion(s):
	"""
	Acquire the version of a cli program.

	param s: The output of the programm version string.

	example: 'gcc --version'
	"""
	regex = r"(\d+)(\.\d+)(\.\d+)?"
	matches = re.finditer(regex, s, re.MULTILINE)
	version = None
	for matchNum, match in enumerate(matches, start=1):
		version = match.group()

	return version


def toString(obj):
	"""
	Convert an object to string representation.

	param obj: The object to convert to string
	"""
	rv = ""
	if obj is None:
		pass
	elif isinstance(obj, list):
		rv = " ".join(obj)
	elif isinstance(obj, set):
		rv = " ".join(obj)
	else:
		rv = str(obj)
	return rv


def run_command(cmd):
	"""
	Run a shell command
	The stdout is shown.

	Returns the error code
	"""

	rv = subprocess.call(cmd, shell=True)
	return rv


def run_command2(cmd):
	"""
	Run a shell command.

	Returns the stdout
	"""

	cmdList = cmd.split(" ")
	rv = None
	try:
		rv = subprocess.run(cmdList, stdout=subprocess.PIPE).stdout.decode("utf-8")
	except FileNotFoundError:
		pass

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


def egrep(keywords, whole_words=False):
	"""
	Runs egrep

	param: keywords       Keywords to search for
	param: whole_words    Search for whole words
	"""
	grep_flags = "-i -nr -R --color --no-messages"

	if whole_words:
		grep_flags += " -w"

	cmd = f"grep -E {grep_flags} '{keywords}' src/ inc/ port/ || true"
	rv = run_command(cmd)
	return rv


def terminal_supports_color():
	"""
	Returns True if the running system's terminal supports color, and False
	otherwise.

	Taken from Django
	https://github.com/django/django/blob/main/django/core/management/color.py
	"""
	plat = sys.platform
	supported_platform = plat != 'Pocket PC' and (plat != 'win32' or 'ANSICON' in os.environ)

	# isatty is not always implemented, #6223.
	is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
	return supported_platform and is_a_tty


def typify_string(string: str):
	"""
	Try to convert a string of builtin python type.

	param: string The string to be converted.

	e.g:
	- 'None' -> None
	- '123' -> 123
	- '3.14' -> 3.14
	- 'string' -> 'string'
	"""

	result_string = None
	try:
		result_string = ast.literal_eval(string)
	except (SyntaxError, ValueError):
		result_string = string

	return result_string
