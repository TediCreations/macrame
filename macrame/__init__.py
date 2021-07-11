#!/usr/bin/env python

import sys

try:
	from pkg_resources import get_distribution, DistributionNotFound
except Exception as e:
	print(e)
	sys.exit(1)

try:
	__version__ = get_distribution(__name__).version
except DistributionNotFound:
	__version__ = "Unknown"

__author__ = "Kanelis Elias"
__email__ = "hkanelhs@yahoo.gr"
__license__ = "MIT"
