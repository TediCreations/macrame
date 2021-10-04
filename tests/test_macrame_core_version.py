import pytest
from macrame.core.version import Version


equal_versionStrings = [
	["0", "0"],
	["0.0", "0.0"],
	["0.0.0", "0.0.0"],
	["1.2.3", "1.2.3"],
	["1.2", "1.2.0"],
	["1.2", "1.2.0"],
	["1.2.3.post13.dev1+g946b55b.d20210910", "1.2.3"]
]

greater_versionStrings = [
	["1", "0"],
	["0.1", "0"],
	["0.0.1", "0"],
	["2", "0"],
	["0.2", "0"],
	["0.0.2", "0"],
	["3", "0"],
	["3.0", "0"],
	["3.0.0", "0"],
	["3.0.1", "0"],
	["3.0.1", "1"],
	["3.0.1", "2"],
	["1.0.1", "1"],
	["1.1.0", "1"],
	["1.1.1", "1"],
	["1.1", "1"],
	["255.255", "255.254"],
	["1.2.3", "1.1.3"],
	["1.3", "1.2.0"],
	["1.4", "1.2.0"],
	["1.2.4.post13.dev1+g946b55b.d20210910", "1.2.3"]
]


class TestClass:

	"""Test cases for core Version"""

	def test_valid_versions(self):

		valid_versionStrings = [
			"0",
			"0.0",
			"0.0.0",
			"1",
			"1.2",
			"1.2.3",
			"255.255.255",
			"0.0.255",
			"255.0.0",
			"0.255.0",
			"0.255.255",
			"255.255.0",
			"0.255.255",
			"9999.9999.9999",
			"0.0.0.post13.dev1+g946b55b.d20210910"
		]

		for string in valid_versionStrings:
			print(f"For string: '{string}'")
			Version(string)

	def test_invalid_versions(self):

		invalid_versionStrings = [
			None,
			"",
			"None",
			"alphabhta",
			".",
			"..",
			"...",
			"1..",
			".1",
			"1.2.",
			".1.2",
			"1.2.3.",
			".1.2.3",
			".1",
			".1.2",
			"a",
			"a.b",
			"a.b.c",
			"a.1",
			"a.1.2",
			"1.a",
			"1.a.2",
			"1.a.b",
			"-1",
			"-",
			"-None",
			"-alphabhta",
			"-.",
			".-.",
			"..-.",
			"-1..",
			".-1",
			"1.-2.",
			".-1.2",
			"1.-2.3.",
			".1.2.-3",
			".-1",
			".1.-2",
			"-a",
			"a.-b",
			"-a.-b.c",
			"a.-1",
			"a.1.-2",
			"-1.a",
			"1.a.-2",
			"-1.a.b",
		]

		for string in invalid_versionStrings:
			print(f"For string: '{string}'")
			with pytest.raises(Exception) as execinfo:
				Version(string)
				print(execinfo)
			assert str(execinfo.value) == 'Invalid version'

	def test_major_minor_patch_assignment(self):

		equal_versionStrings = [
			["0", [0, 0, 0]],
			["0.0", [0, 0, 0]],
			["0.0.0", [0, 0, 0]],
			["1", [1, 0, 0]],
			["1.2", [1, 2, 0]],
			["1.2.3", [1, 2, 3]],
			["1.2.3.post13.dev1+g946b55b.d20210910", [1, 2, 3]]
		]

		for element in equal_versionStrings:
			s = element[0]
			major = element[1][0]
			minor = element[1][1]
			patch = element[1][2]

			version = Version(s)

			print(f"Comparing: '{element}'")
			assert version.major == major
			assert version.minor == minor
			assert version.patch == patch

	def test_equal_versions(self):

		for element in equal_versionStrings:
			s_1 = element[0]
			s_2 = element[1]
			v_1 = Version(s_1)
			v_2 = Version(s_2)

			print(f"Comparing: '{element}'\t| '{v_1}' == '{v_2}'")
			assert v_1 == v_2

	def test_not_equal_versions(self):

		# We use greater as the sets are also not equal
		for element in greater_versionStrings:
			s_1 = element[0]
			s_2 = element[1]
			v_1 = Version(s_1)
			v_2 = Version(s_2)

			print(f"Comparing: '{element}'\t| '{v_1}' != '{v_2}'")
			assert v_1 != v_2

	def test_greater_version(self):

		for element in greater_versionStrings:
			s_1 = element[0]
			s_2 = element[1]
			v_1 = Version(s_1)
			v_2 = Version(s_2)

			print(f"Comparing: '{element}'\t| '{v_1}' > '{v_2}'")
			assert v_1 > v_2

	def test_less_version(self):

		# We use greater and compare with the opposing sets
		for element in greater_versionStrings:
			s_1 = element[1]  # Here
			s_2 = element[0]  # And here
			v_1 = Version(s_1)
			v_2 = Version(s_2)

			print(f"Comparing: '{element}'\t| '{v_1}' < '{v_2}'")
			assert v_1 < v_2

	def test_less_equal_version(self):

		for element in equal_versionStrings:
			s_1 = element[0]
			s_2 = element[1]
			v_1 = Version(s_1)
			v_2 = Version(s_2)

			print(f"Comparing: '{element}'\t| '{v_1}' <= '{v_2}'")
			assert v_1 <= v_2

		for element in greater_versionStrings:
			s_1 = element[1]
			s_2 = element[0]
			v_1 = Version(s_1)
			v_2 = Version(s_2)

			print(f"Comparing: '{element}'\t| '{v_1}' <= '{v_2}'")
			assert v_1 <= v_2

	def test_greater_equal_version(self):

		for element in equal_versionStrings:
			s_1 = element[0]
			s_2 = element[1]
			v_1 = Version(s_1)
			v_2 = Version(s_2)

			print(f"Comparing: '{element}'\t| '{v_1}' >= '{v_2}'")
			assert v_1 >= v_2

		for element in greater_versionStrings:
			s_1 = element[0]
			s_2 = element[1]
			v_1 = Version(s_1)
			v_2 = Version(s_2)

			print(f"Comparing: '{element}'\t| '{v_1}' >= '{v_2}'")
			assert v_1 >= v_2
