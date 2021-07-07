#!/usr/bin/env python3

import os

try:
	from pkg_resources import get_distribution, DistributionNotFound
except Exception as e:
	print(e)
	os.exit(1)

__version__ = "?"
try:
	__version__ = get_distribution(__name__).version
except DistributionNotFound:
	pass

__author__ = "Kanelis Elias"
__email__ = "hkanelhs@yahoo.gr"
__license__ = "MIT"

from .app import App
