#!/usr/bin/env python

import subprocess


def run_command(cmd):
	"""
	Run a shell command
	"""

	rv = subprocess.call(cmd, shell=True)
	return rv
