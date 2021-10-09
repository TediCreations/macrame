import os
import re
import ast
from abc import ABC, abstractmethod
from ..core.version import Version
# from ..core.utils import typify_string
from ..core.utils import run_command2
from ..core.utils import acquireCliProgramVersion
from ..core.utils import which
from ..core.colors import Color


class NotValidConfiguration(Exception):
	"""Exception for when a config is not valid."""

	def __init__(self, msg):
		message = str(msg)
		super().__init__(message)


class MandatoryConfigAttributeMissing(Exception):
	"""Exception for when a config is missing a mandatory attribute."""

	def __init__(self, config, attribute: str):
		message = f"'{config.__class__.__name__}' is missing mandatory attribute '{attribute}'"
		super().__init__(message)


class InvalidAttribute(Exception):
	"""Exception for when a config has an invalid attribute."""

	def __init__(self, config, attribute: str):
		message = f"'{config.__class__.__name__}.{attribute}' is invalid"
		super().__init__(message)


class OperationOnIncompatibleConfigs(Exception):
	"""Exception for when a config can not handle an operation."""

	def __init__(self, msg):
		message = str(msg)
		super().__init__(message)


class Config(ABC):

	"""Base class for all configurations."""

	def __init__(self, config) -> None:
		"""
		Initialize tools config.

		params config: Dictionary that holds the tool configuration
		"""

		# Validate configuration
		if not isinstance(config, dict):
			raise TypeError(f"Not a valid '{self.__class__.__name__}' configuration")

		# Automatically load dictionary keys as members
		for k, v in config.items():
			# TODO: Use typify_strings
			#
			# value = typify_string(v)
			# print(f"Setting: {k}: {v} | {value}")
			#
			value = v
			setattr(self, k, value)

		# Verify mandatory config attributes
		mandatory_attribute_list = self.get_mandatory_atrributes_list()
		if mandatory_attribute_list is not None:
			for mandatory_attribute in mandatory_attribute_list:
				self._verify_mandatory_attribute(mandatory_attribute)

		# Verify optional config attributes
		optional_attribute_list = self.get_optional_atrributes_list()
		if optional_attribute_list is not None:
			for optional_attribute in optional_attribute_list:
				self._verify_optional_attribute_or_None(optional_attribute)

		# Check rules
		self.rule_checks()

	def __str__(self):
		"""Get string that represents the object."""

		s = f"[{Color.BLUE}{self.__class__.__name__}{Color.RESET}]\n"
		for k, v in self.__dict__.items():
			s += f"{k}: {Color.YELLOW}{v}{Color.RESET}\n"

		return s

	@abstractmethod
	def getLabel(self) -> str:
		"""Return the label(name) of the config"""

	@abstractmethod
	def get_mandatory_atrributes_list(self) -> list:
		"""Return the mandatory attributes."""

	@abstractmethod
	def get_optional_atrributes_list(self) -> list:
		"""Return the optional attributes."""

	@abstractmethod
	def rule_checks(self) -> None:
		"""Perform custom tests at init."""

	def _verify_mandatory_attribute(self, attribute_string: str):
		"""
		Set an attribute given the string representation.

		attribute_string: The atribute string representation
		"""
		try:
			getattr(self, attribute_string)
		except AttributeError as e:
			raise MandatoryConfigAttributeMissing(self, attribute_string) from e

	def _verify_optional_attribute_or_None(self, attribute_string: str):
		"""
		Given a an optional attribute string representation,
		assign it into None if it is not provided
		or the actual value.

		attribute_string: The attribute string representation
		"""
		value = None
		try:
			value = getattr(self, attribute_string)
		except AttributeError:
			value = None

		setattr(self, attribute_string, value)

	# TODO: Refactor the use of this function
	def _parse_env_variables(self, test_str) -> str:
		"""
		Parses an environmental variable in the config
		and returns the match.

		param: test_str The string to apply the regular expression to.
		"""

		reply = test_str

		regex = r"(?:\$\{)(.*)(?:\})"  # {}
		# regex = r"(?:\$\()(.*)(?:\))"  # ()
		matches = re.finditer(regex, test_str, re.MULTILINE)

		for _, match in enumerate(matches, start=1):
			# Find env variable
			match_str = match.group(1)
			value_str = os.getenv(match_str)
			if value_str is None:
				value_str = ""

			# Replace
			# Beware that curly braces below are escaped
			reply = reply.replace(f"${'{'}{match_str}{'}'}", value_str)

		return reply


class Tool(Config):

	"""
	Configuration class for Tools.
	"""

	def getLabel(self) -> str:
		"""Return the label(name) of the config."""
		return self.name

	def get_mandatory_atrributes_list(self) -> list:
		"""Return the mandatory attributes."""

		attribute_list = [
			"name"
		]

		return attribute_list

	def get_optional_atrributes_list(self) -> list:
		"""Return the optional attributes."""

		attribute_list = [
			"arg",
			"compare",
			"version"
		]

		return attribute_list

	def rule_checks(self) -> None:
		"""Perform custom tests at init."""

	def __add__(self, other):
		# TODO: Add properly
		return self

	def check(self) -> None:
		"""
		Checks a tools existance in the system
		and its version.
		"""
		# Check existance
		isAvailable = which(self.name)
		if isAvailable is None:
			raise Exception(f"{self.name} not found!")

		# Check version
		cmd = self.name + " " + self.arg

		raw_version_string = str(run_command2(cmd))
		parsed_version_string = acquireCliProgramVersion(raw_version_string)

		actual_version = Version(parsed_version_string)
		desired_version = Version(self.version)

		result = False
		if self.compare == "==":
			result = actual_version == desired_version
		elif self.compare == ">=":
			result = actual_version >= desired_version
		elif self.compare == ">":
			result = actual_version > desired_version
		elif self.compare == "<=":
			result = actual_version <= desired_version
		elif self.compare == "<":
			result = actual_version < desired_version

		if result is False:
			raise Exception(f"{self.name} is not {self.compare} {self.version}")


class Environment(Config):
	"""Configuration class for ennvironment variables."""

	available_methods = [None, "append"]

	def getLabel(self) -> str:
		"""Return the label(name) of the config."""

		return self.name

	def get_mandatory_atrributes_list(self) -> list:
		"""Return the mandatory attributes"""

		attribute_list = [
			"name",
			"value"
		]

		return attribute_list

	def get_optional_atrributes_list(self) -> list:
		"""Return the optional attributes."""

		attribute_list = [
			"condition",
			"method",
			"description"
		]

		return attribute_list

	def rule_checks(self) -> None:
		"""Perform custom tests at init."""

		if self.method not in self.available_methods:
			print(f"self.method: {self.method}")
			raise InvalidAttribute(self, "method")

	# TODO: Continue with features (condition)
	def __add__(self, other):

		# Test if merge is possible
		if self.name != other.name:
			raise OperationOnIncompatibleConfigs(f"Trying to add '{self.name}' + '{other.name}' environment variables")

		newDict = {
			"condition": "True",
			"name": self.name,
			"value": None,
			"description": None,
			"method": None
		}

		# Test other
		if other.method == "append":
			newDict["value"] = self.value + " " + other.value
		else:
			newDict["value"] = other.value

		newDict["method"] = other.method

		rv = Environment(newDict)

		return rv

	def register(self) -> None:
		"""Registers the environment variable."""

		condition_result = True
		if self.condition:
			condition = self.condition
			condition = self._parse_env_variables(condition)

			try:
				condition_result = ast.literal_eval(condition)
			except (NameError, SyntaxError) as e:
				raise NotValidConfiguration("Invalid syntax in Environment variable condition: ({self.condition})") from e

		if condition_result:
			value = self._parse_env_variables(self.value)
			new_value = value

			if self.method == "append":
				old_value = os.environ.get(self.name)
				if old_value:
					new_value = os.environ[self.name] + " " + new_value

			os.environ[self.name] = new_value


class MakefileRule(Config):

	"""
	Configuration class for a Makefile rule.

	targets: prerequisites
		commands
	"""

	def getLabel(self) -> str:
		"""Return the label(name) of the config"""

		return self.targets

	def get_mandatory_atrributes_list(self) -> list:
		"""Return the mandatory attributes."""

		attribute_list = [
			"targets",
			"prerequisites"
		]

		return attribute_list

	def get_optional_atrributes_list(self) -> list:
		"""Return the optional attributes."""

		attribute_list = [
			"command",
			"description"
		]

		return attribute_list

	def rule_checks(self) -> None:
		"""Perform custom tests at init."""
		pass

	def generate_rule(self) -> None:
		"""Do the config."""
		# project_dirpath = "XXX"
		# print(f"Project: {project_dirpath}")

		txt = ""
		if self.phony:
			txt += f"PHONY: {self.targets}\n"
		txt += f"{self.targets}:"
		if self.prerequisites:
			txt += f" {self.prerequisites}\n"
		else:
			txt += "\n"
		if self.command:
			stripped_command = self.command.rstrip()
			txt += f"{stripped_command}\n"
		else:
			txt += ":\n"
		txt += "\n"

		return txt


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

		# Generated makefile
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

		# Create the makefile directory ifit does not exist
		if not os.path.exists(makefile_dirpath):
			os.makedirs(makefile_dirpath)
			# print(f"The new directory '{makefile_dirpath}' is created!")

		# Check if file exists
		if os.path.isfile(makefile_filepath):
			# Try to update it
			with open(makefile_filepath, 'r+') as f:
				makefile_text = f.read()

				if makefile_text != self.makefile_text:
					# Differences were found
					f.seek(0)
					f.write(self.makefile_text)
					f.truncate()
					# print(f"Updated {makefile_filepath}")
		else:
			# Write it since it does not exist
			with open(makefile_filepath, 'w') as f:
				f.write(self.makefile_text)
				# print(f"Wrote {makefile_filepath}")
