#!/usr/bin/env python

"""
Make and makefile manager
"""

import os
import toml
from .adt import ConfigLoader
from .adt import ConfigProcessor
from .adt import BuildManager
from ..core.utils import run_command
from ..core.utils import listPortNames
from ..resource import get_abs_resourse_path
from ..configuration.config.tool import Tool
from ..configuration.config.environment import Environment
from ..configuration.config.makefilerule import MakefileRule
from ..configuration.configurator import Configurator


def is_makefile_exist():
	"""
	Checks is a local Makefile exists in the current working directory
	"""
	rv = False
	if os.path.isfile("Makefile"):
		rv = True

	return rv


class MakefileConfigLoader(ConfigLoader):  # pylint: disable=R0903

	"""Loader for the config of Makefile based builds."""

	def __init__(self, project_path: str, port_name: str) -> None:
		"""
		Constructor for the makefile loader

		params: project_path: The absolute directory to the project path
		params: port_name: The port name or None
		"""
		self.project_path = project_path
		self.port_name = port_name

		self.config_list = []

		# Load the config
		self._load()

	def _load(self) -> None:
		"""Loads the config."""

		# Load config
		# 1st (mandatory/default)
		dir_path = os.path.dirname(os.path.realpath(__file__))
		file_path = os.path.join(dir_path, "default.toml")
		system_config = toml.load(file_path)
		self.config_list.append(system_config)

		# Root config
		# 2nd (optional)
		root_config = None
		if root_config is not None:
			self.config_list.append(root_config)

		# Load port environment variables
		# 3nd (optional)
		port_config = None
		if self.port_name is not None:
			dir_path = os.path.join(self.project_path, "port", self.port_name)
			file_path = os.path.join(dir_path, "config.toml")

			if os.path.isfile(file_path):
				port_config = toml.load(file_path)
				self.config_list.append(port_config)

		return self.config_list

	def get(self) -> list:
		"""Get the list of configs."""

		return self.config_list


class MakefileConfigProcessor(ConfigProcessor):
	"""Processor for the config of Makefile based builds."""

	def __init__(self, project_path: str, port_name: str, config_loader: ConfigLoader) -> None:
		"""
		Initialises the makefile config processor.

		params: project_path: The absolute directory to the project path
		params: port_name: The port name or None
		param: config_loader: The configuration loader.
		"""
		self.project_path = project_path
		self.port_name = port_name

		# List of supported config types
		config_type_list = [Tool, Environment, MakefileRule]

		# Turn config list into a dictionary
		self.config_type_dict = {}
		for configType in config_type_list:
			config_type_name = configType.__name__
			self.config_type_dict[config_type_name] = configType

		# Appent partial config to global config
		self.config = {}
		config_list = config_loader.get()
		for config in config_list:
			self._append_to_config(config)

	def _append_to_config(self, partial_config: dict) -> None:
		"""
		Appent partial config to global config.

		param: partial_config Partial config to be appented
		"""

		if partial_config is None:
			return

		for config_name in partial_config:
			config_list = partial_config[config_name]
			for config_element in config_list:

				# Convert the dict to a valid configuration
				try:
					config_obj = self.config_type_dict[config_name](config_element)
				except KeyError:
					# Skip not known configs
					# TODO: Should an unknown config cause an error reaction?
					continue

				# Create dict if it does not exist
				if config_name not in self.config:
					self.config[config_name] = {}
				config_type = self.config[config_name]

				# Combine
				name_of_type = config_obj.get_label()
				if name_of_type not in config_type:
					config_type[name_of_type] = config_obj
				else:
					config_type[name_of_type] = config_type[name_of_type] + config_obj

	def __str__(self):

		txt = ""
		for config_category_name, config_category in self.config.items():
			for config_category_key, _ in config_category.items():
				txt += f"[{config_category_name}][{config_category_key}]\n"

		return txt

	def handle(self) -> None:
		"""Applies the config."""

		configurator = Configurator(self.project_path, self.port_name)

		for config_type_name, config_type in self.config_type_dict.items():

			if config_type_name in self.config:
				config_dict = self.config[config_type_name]

				for key, _ in config_dict.items():
					env_var = config_dict[key]
					configurator.load(env_var)

		configurator.handle()


class MakefileBuildManager(BuildManager):
	"""Manages the way that Make is called."""

	def __init__(self, project_path, port_name=None, use_local_makefile=True) -> None:
		"""
		Initialization.

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

		# Load the config
		config_loader = MakefileConfigLoader(project_path, port_name)

		# Process the config
		config_processor = MakefileConfigProcessor(project_path, port_name, config_loader)

		self._set_env_variables(config_processor, makefile_dirpath, project_path)

	def _set_env_variables(self, config_processor: ConfigProcessor, makefile_dirpath: str, project_path: str) -> None:
		"""
		Set the environment variables

		param: configProcessor The configuration processor
		param: makefile_dirpath The path of the directory that Makefile is located
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

		# Set environment variables
		config_processor.handle()

		# Find all files
		as_srcs_list = []
		c_srcs_list = []
		cxx_srcs_list = []

		for path, _, files in os.walk("src"):
			for name in files:
				relative_filepath = os.path.join(path, name)
				if relative_filepath.endswith(".s"):
					as_srcs_list.append(relative_filepath)
				elif relative_filepath.endswith(".c"):
					c_srcs_list.append(relative_filepath)
				elif relative_filepath.endswith(".cpp"):
					cxx_srcs_list.append(relative_filepath)

		if self.port_name is not None:
			for path, _, files in os.walk("port/" + self.port_name):
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
		Checks if the project meets the standards
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
