#!/usr/bin/env python

"""
Resourse manager
"""

import os


def get_abs_resourse_path(rel_resourse_path: str) -> str:
	"""
	Get the absolute path of a resourse.

	Resourse is a file located in the static directory.
	"""

	resourse_py_path = os.path.dirname(os.path.abspath(__file__))
	root_path = os.path.abspath(os.path.join(resourse_py_path, "../static"))
	abs_resourse_path = os.path.join(root_path, rel_resourse_path)
	return abs_resourse_path
