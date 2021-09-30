#!/usr/bin/env python

"""
Make and makefile manager
"""

import os
import toml
from .manager import BuildManager
from ..core.utils import run_command
from ..core.utils import listPortNames
from ..resource import get_abs_resourse_path
from ..configuration.config import Environment


def is_makefile_exist():
	"""
	Checks is a local Makefile exists in the current working directory
	"""
	rv = False
	if os.path.isfile("Makefile"):
		rv = True

	return rv


class MakefileBuildManager(BuildManager):
	"""
	Manages the way that Make is called
	"""

	def __init__(self, project_path, port_name=None, use_local_makefile=True):
		"""
		Initialization

		param: project_path The root directory of the project.
		param: port_name   The name of the port.
		param: use_local_makefile   True to select local makefile. False to select static makefile.
		"""

		# Select makefile
		if port_name == "":
			self.port_name = None
		else:
			self.port_name = port_name

		# Decide upon local or remote makefile
		makefile_dirpath = get_abs_resourse_path("Makefile")
		self.makefile_path = os.path.join(makefile_dirpath, "Makefile")
		if is_makefile_exist() is True and use_local_makefile is True:
			self.makefile_path = "Makefile"

		# List ports
		self.ports = listPortNames()

		# Validation
		if self.port_name is None and self.ports is not None:
			# There are available ports but the used did not select any
			# So we assign the first port
			self.port_name = self.ports[0]

		self._set_env_variables(makefile_dirpath, project_path)

	def _set_env_variables(self, makefile_dirpath, project_path):
		"""
		Set the environment variables

		param: makefile_dirpath The path of the direcoty that Makefile is located
		param: project_path The path of the project to be build
		"""

		# Environment variables to be cleared
		env_var_list = [
			"PROJ_NAME",
			"TARGET",
			"PORT_NAME",
			# "AUX",
			"BUILDSYSTEM_DIRPATH",
			"RUN_CMD",
			"SIZE_CMD",
			"AS",
			"CC",
			"CXX",
			"LD",
			"SZ",
			"OC",
			"NM",
			"ASFLAGS",
			"CFLAGS",
			"CXXFLAGS",
			"CPPFLAGS",
			"LDFLAGS",
		]

		# Clear environment variable list
		for env_var in env_var_list:
			os.unsetenv(env_var)

		# Setup
		proj_name = os.path.basename(project_path)
		os.environ["PROJ_NAME"] = proj_name
		os.environ["TARGET"] = "dbg"
		if self.port_name is not None:
			os.environ["PORT_NAME"] = self.port_name

		os.environ["BUILDSYSTEM_DIRPATH"] = makefile_dirpath

		# Load global environment variables
		dir_path = os.path.dirname(os.path.realpath(__file__))
		file_path = os.path.join(dir_path, "env.toml")
		parsed_toml = toml.load(file_path)

		# Set environment variables
		for env_var in parsed_toml["Environment"]:
			e = Environment(env_var)
			e.register()

		# Load port environment variables
		if self.port_name is not None:
			dir_path = os.path.join(project_path, "port", self.port_name)
			file_path = os.path.join(dir_path, "config.toml")

			if os.path.isfile(file_path):
				parsed_toml = toml.load(file_path)

				# Set environment variables
				for env_var in parsed_toml["Environment"]:
					e = Environment(env_var)
					e.register()

		# Find all files
		as_srcs_list = list()
		c_srcs_list = list()
		cxx_srcs_list = list()

		for path, subdirs, files in os.walk("src"):
			for name in files:
				relative_filepath = os.path.join(path, name)
				if relative_filepath.endswith(".s"):
					as_srcs_list.append(relative_filepath)
				elif relative_filepath.endswith(".c"):
					c_srcs_list.append(relative_filepath)
				elif relative_filepath.endswith(".cpp"):
					cxx_srcs_list.append(relative_filepath)

		if self.port_name is not None:
			for path, subdirs, files in os.walk("port/" + self.port_name):
				for name in files:
					relative_filepath = os.path.join(path, name)
					if relative_filepath.endswith(".s"):
						as_srcs_list.append(relative_filepath)
					elif relative_filepath.endswith(".c"):
						c_srcs_list.append(relative_filepath)
					elif relative_filepath.endswith(".cpp"):
						cxx_srcs_list.append(relative_filepath)

		# Sort the file lists
		as_srcs_list.sort()
		c_srcs_list.sort()
		cxx_srcs_list.sort()

		# Extract the environment variables from assembly files
		as_srcs = ""
		for src_file in as_srcs_list:
			as_srcs += src_file + " "
		as_srcs = as_srcs.rstrip(" ")
		os.environ["AS_SRCs"] = as_srcs

		# Extract the environment variables from C files
		c_srcs = ""
		for src_file in c_srcs_list:
			c_srcs += src_file + " "
		c_srcs = c_srcs.rstrip(" ")
		os.environ["C_SRCs"] = c_srcs

		# Extract the environment variables from C++ files
		cxx_srcs = ""
		for src_file in cxx_srcs_list:
			cxx_srcs += src_file + " "
		cxx_srcs = cxx_srcs.rstrip(" ")
		os.environ["CXX_SRCs"] = cxx_srcs

		# Delete
		# print(f"'{as_srcs}'")
		# print(f"'{c_srcs}'")
		# print(f"'{cxx_srcs}'")

	@staticmethod
	def is_project_usable(project_path) -> bool:
		"""
		Checks is the project meets the standards
		to use this build manager
		"""
		rv = False
		src_directory = os.path.join(project_path, "src")
		if os.path.isdir(src_directory):
			rv = True

		return rv

	def build(self):
		"""
		Builds the project
		"""
		# print("RUN_CMD: ", os.environ.get("RUN_CMD"))
		# for k, v in sorted(os.environ.items()):
		# 	print(k + ':', v)
		# print('\n')
		rv = run_command(f"make -f {self.makefile_path}")
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
		rv = run_command(f"make -f {self.makefile_path} run")
		return rv
