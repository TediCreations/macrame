#!/usr/bin/env python

"""Configurator."""

import os
from .adt import Config
from .config.tool import Tool
from .config.environment import Environment
from .config.makefilerule import MakefileRule


class Configurator:
	"""Configures a config."""

	def __init__(self, project_path: str, port_name: str) -> None:
		"""
		Initialization of the configurator.

		param: project_path The root directory of the project.
		param: port_name The name of the port.
		"""
		self.project_path = project_path
		self.port_name = port_name

		# Now the makefile content (text) is empty
		# but it will be filled with the rules
		self.makefile_text = ""

	def load(self, config: Config) -> None:
		"""
		Loads a given config.

		param: config The config object
		"""
		config_type = type(config)
		if config_type is Tool:
			config.check()
		elif config_type is Environment:
			config.register()
		elif config_type is MakefileRule:
			rule = config.generate_rule()
			self.makefile_text += rule
		else:
			raise Exception(f"Not able to configure '{config_type}'")

	def handle(self) -> None:
		"""Handles a given config."""

		# TODO: Add support for TARGET selection
		target = "dbg"

		# Generate the Makefile
		if self.port_name is not None:
			makefile_dirpath = os.path.join(self.project_path, "gen", self.port_name, target)
		else:
			makefile_dirpath = os.path.join(self.project_path, "gen", target)

		makefile_filepath = os.path.join(makefile_dirpath, "Makefile")

		# Create the makefile directory if it does not exist
		if not os.path.exists(makefile_dirpath):
			os.makedirs(makefile_dirpath)

		# Check if file exists
		if os.path.isfile(makefile_filepath):
			# Try to update it
			with open(makefile_filepath, 'r+', encoding="utf-8") as makefile_f:
				makefile_text = makefile_f.read()

				if makefile_text != self.makefile_text:
					# Differences were found
					# Shall update the makefile
					makefile_f.seek(0)
					makefile_f.write(self.makefile_text)
					makefile_f.truncate()
		else:
			# Makefile does not exist
			# Shall write a new makefile
			with open(makefile_filepath, 'w', encoding="utf-8") as makefile_f:
				makefile_f.write(self.makefile_text)
