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

		for d in equal_versionStrings:
			s = d[0]
			major = d[1][0]
			minor = d[1][1]
			patch = d[1][2]

			v = Version(s)

			print(f"Comparing: '{d}'")
			assert v.major == major
			assert v.minor == minor
			assert v.patch == patch

	def test_equal_versions(self):

		for d in equal_versionStrings:
			s1 = d[0]
			s2 = d[1]
			v1 = Version(s1)
			v2 = Version(s2)

			print(f"Comparing: '{d}'\t| '{v1}' == '{v2}'")
			assert v1 == v2

	def test_not_equal_versions(self):

		# We use greater as the sets are also not equal
		for d in greater_versionStrings:
			s1 = d[0]
			s2 = d[1]
			v1 = Version(s1)
			v2 = Version(s2)

			print(f"Comparing: '{d}'\t| '{v1}' != '{v2}'")
			assert v1 != v2

	def test_greater_version(self):

		for d in greater_versionStrings:
			s1 = d[0]
			s2 = d[1]
			v1 = Version(s1)
			v2 = Version(s2)

			print(f"Comparing: '{d}'\t| '{v1}' > '{v2}'")
			assert v1 > v2

	def test_less_version(self):

		# We use greater and compare with the opposing sets
		for d in greater_versionStrings:
			s1 = d[1]  # Here
			s2 = d[0]  # And here
			v1 = Version(s1)
			v2 = Version(s2)

			print(f"Comparing: '{d}'\t| '{v1}' < '{v2}'")
			assert v1 < v2

	def test_less_equal_version(self):

		for d in equal_versionStrings:
			s1 = d[0]
			s2 = d[1]
			v1 = Version(s1)
			v2 = Version(s2)

			print(f"Comparing: '{d}'\t| '{v1}' <= '{v2}'")
			assert v1 <= v2

		for d in greater_versionStrings:
			s1 = d[1]
			s2 = d[0]
			v1 = Version(s1)
			v2 = Version(s2)

			print(f"Comparing: '{d}'\t| '{v1}' <= '{v2}'")
			assert v1 <= v2

	def test_greater_equal_version(self):

		for d in equal_versionStrings:
			s1 = d[0]
			s2 = d[1]
			v1 = Version(s1)
			v2 = Version(s2)

			print(f"Comparing: '{d}'\t| '{v1}' >= '{v2}'")
			assert v1 >= v2

		for d in greater_versionStrings:
			s1 = d[0]
			s2 = d[1]
			v1 = Version(s1)
			v2 = Version(s2)

			print(f"Comparing: '{d}'\t| '{v1}' >= '{v2}'")
			assert v1 >= v2
