import os
import sys
import re
from abc import ABC
from ..core.version import Version
from ..core.utils import run_command2
from ..core.utils import acquireCliProgramVersion


class Config(ABC):

	"""
	Base class for all configurations
	"""

	def __init__(self, config):
		"""
		Initialize tools

		params config: Dictionary that holds the tool configuration
		"""

		# Validate configuration
		if not isinstance(config, dict):
			raise Exception(f"Not a valid '{self.__class__.__name__}' configuration")

		# Automatically load dictionary keys as memebers
		for k, v in config.items():
			setattr(self, k, v)

	def __str__(self):

		s = f"[{self.__class__.__name__}]\n"
		for k, v in self.__dict__.items():
			s += f"{k}: {v}\n"

		return s

	def _optional_attribute_or_None(self, self_attribute: str):
		"""
		Get the string of an optional variable
		and return None if it is not provided
		or the actual value

		param: self_attribute The optional self attribute
		"""
		value = None
		try:
			value = eval(self_attribute)
		except AttributeError:
			value = None

		return value

	def _parse_env_variables(self, test_str):

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
	Configuration class for Tools
	"""

	def check(self):
		"""
		Checks a tools existance in the system
		and its version
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

	"""
	Configuration class for ennvironment variables
	"""

	def register(self) -> None:
		"""
		Registers the environment variable
		"""
		self.condition = self._optional_attribute_or_None("self.condition")
		self.type = self._optional_attribute_or_None("self.type")

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

			if self.type == "append":
				old_value = os.environ.get(self.name)
				if old_value:
					new_value = os.environ[self.name] + " " + new_value

			os.environ[self.name] = new_value
