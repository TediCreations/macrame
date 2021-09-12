class Version():

	major = None
	minor = None
	patch = None
	# prerelease = None
	# build = None

	def __init__(self, string_with_version):
		"""
		Initialize the version

		param: string that holds the version
		"""
		self.major, self.minor, self.patch = self._parse(string_with_version)

	def __str__(self):
		"""
		Print the version
		"""
		s = ""
		if self.major is not None:
			s += str(self.major)
			if self.minor is not None:
				s += "." + str(self.minor)
				if self.patch is not None:
					s += "." + str(self.patch)
		return s

	def __eq__(self, other):
		"""
		Overloads equality operator (==)
		"""

		if self.major == other.major and \
		   self.minor == other.minor and \
		   self.patch == other.patch:
			return True

		return False

	def __ne__(self, other):
		"""
		Overloads not equal operator (!=)
		"""

		if self.major == other.major and \
		   self.minor == other.minor and \
		   self.patch == other.patch:
			return False

		return True

	def __gt__(self, other):
		"""
		Overloads greater operator (>)
		"""

		if self.major > other.major:
			return True
		elif self.major == other.major:
			if self.minor > other.minor:
				return True
			elif self.minor == other.minor:
				if self.patch > other.patch:
					return True

		return False

	def __ge__(self, other):
		"""
		Overloads greater or equal operator (>=)
		"""

		if self.major > other.major:
			return True
		elif self.major == other.major:
			if self.minor > other.minor:
				return True
			elif self.minor == other.minor:
				if self.patch > other.patch:
					return True
				elif self.patch == other.patch:
					return True

		return False

	def __lt__(self, other):
		"""
		Overloads less operator (<)
		"""

		if self.major < other.major:
			return True
		elif self.major == other.major:
			if self.minor < other.minor:
				return True
			elif self.minor == other.minor:
				if self.patch < other.patch:
					return True

		return False

	def __le__(self, other):
		"""
		Overloads less or equal operator (<=)
		"""

		if self.major < other.major:
			return True
		elif self.major == other.major:
			if self.minor < other.minor:
				return True
			elif self.minor == other.minor:
				if self.patch < other.patch:
					return True
				elif self.patch == other.patch:
					return True

		return False

	def _parse(self, string_with_version):

		# We begin with a valid version
		# Until it turns out to be invalid in the process
		major = 0
		minor = 0
		patch = 0

		# We check for argument validity
		if not isinstance(string_with_version, str):
			raise Exception("Invalid version")
		elif string_with_version == "":
			raise Exception("Invalid version")

		if string_with_version[-1] == '.':
			raise Exception("Invalid version")

		# Since the version is a string we now try to parse it
		versionList = string_with_version.split('.', 3)

		def integer_None_or_zero(v):
			rv = 0

			try:
				rv = int(v)
			except Exception:
				rv = None

			if rv is not None:
				if rv < 0:
					rv = None

			return rv

			"""
			if v is not None:
				try:
					rv = int(v)
				except Exception:
					rv = None
			return rv
			"""

		i = 0
		for n in versionList:

			if i == 0:
				major = integer_None_or_zero(n)
			elif i == 1:
				minor = integer_None_or_zero(n)
			elif i == 2:
				patch = integer_None_or_zero(n)
			# elif i == 3:
			# 	version["prerelease"] = n
			# elif i == 4:
			# 	version["build"] = n
			else:
				pass
			i += 1

		if major is None or minor is None or patch is None:
			raise Exception("Invalid version")

		return major, minor, patch
