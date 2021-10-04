import os
import sys
import re
from abc import ABC, abstractmethod
from ..core.version import Version
# from ..core.utils import typify_string
from ..core.utils import run_command2
from ..core.utils import acquireCliProgramVersion
from ..core.colors import BLUE, YELLOW, RESET


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

		s = f"[{BLUE}{self.__class__.__name__}{RESET}]\n"
		for k, v in self.__dict__.items():
			s += f"{k}: {YELLOW}{v}{RESET}\n"

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

	@abstractmethod
	def doit(self) -> None:
		"""Do the config."""

	def _verify_mandatory_attribute(self, attribute_string: str):
		"""
		Set an attribute given the string representation.

		attribute_string: The atribute string representation
		"""
		try:
			getattr(self, attribute_string)
		except AttributeError:
			raise MandatoryConfigAttributeMissing(self, attribute_string)

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

		for matchNum, match in enumerate(matches, start=1):
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
		return None

	def get_optional_atrributes_list(self) -> list:
		"""Return the optional attributes."""
		return None

	def rule_checks(self) -> None:
		"""Perform custom tests at init."""
		pass

	def doit(self) -> None:
		"""Do the config."""
		raise NotImplementedError()

	def __add__(self, other):
		return self

	def check(self) -> bool:
		"""
		Checks a tools existance in the system
		and its version.
		"""

		cmd = self.name + " " + self.arg

		string_with_actual_version = str(run_command2(cmd))

		string_with_actual_version = acquireCliProgramVersion(string_with_actual_version)

		result = False
		try:
			actual_version = Version(string_with_actual_version)
		except Exception:
			print(f"'{self.name}' is not available")
			result = None
		desired_version = Version(self.version)

		if result is not None:
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

		return result


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

	def doit(self) -> None:
		"""Do the config."""

		self._register()

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

	def _register(self) -> None:
		"""Registers the environment variable."""

		condition_result = True
		if self.condition:
			condition = self.condition
			condition = self._parse_env_variables(condition)

			try:
				condition_result = eval(condition)
			except NameError as e:
				# TODO: reraise Exception
				print(f"'{e}' in Environment variable condition: ({self.condition})")
				sys.exit(1)
			except SyntaxError:
				# TODO: reraise Exception
				print(f"Invalid syntax in Environment variable condition: ({self.condition})")
				sys.exit(1)

		if condition_result:
			value = self._parse_env_variables(self.value)
			new_value = value

			if self.method == "append":
				old_value = os.environ.get(self.name)
				if old_value:
					new_value = os.environ[self.name] + " " + new_value

			os.environ[self.name] = new_value
