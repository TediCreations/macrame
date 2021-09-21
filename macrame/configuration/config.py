from ..core.version import Version
from ..core.utils import run_command2
from ..core.utils import acquireCliProgramVersion

from abc import ABC


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
