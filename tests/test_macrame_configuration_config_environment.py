import pytest

from macrame.configuration.config.environment import Environment
from macrame.configuration.exceptions import MandatoryConfigAttributeMissing
from macrame.configuration.exceptions import InvalidAttribute
from macrame.configuration.exceptions import OperationOnIncompatibleConfigs


def assert_environment_dict_equal(environment_object, desired_dict):
	assert environment_object.name == desired_dict["name"]
	assert environment_object.value == desired_dict["value"]

	assert environment_object.condition == desired_dict["condition"]
	assert environment_object.description == desired_dict["description"]
	assert environment_object.method == desired_dict["method"]


class TestClass:

	def test_shall_only_use_a_dictionary_when_initialising(self):
		data = 3
		with pytest.raises(TypeError) as execinfo:
			Environment(data)
		assert str(execinfo.value) == "Not a valid 'Environment' configuration"

	def test_shall_get_valid_name_when_calling_getName(self):

		data = {
			'condition': "False",
			'name': "CCACHE",
			'value': "ccache",
			'description': "Default cache tool for the build toolchain"
		}

		a = Environment(data)
		assert a.get_label() == data['name']

	def test_shall_raise_exception_when_name_is_not_configured(self):

		data = {
			'condition': "False",
			'value': "ccache",
			'description': "Default cache tool for the build toolchain"
		}

		with pytest.raises(MandatoryConfigAttributeMissing) as execinfo:
			Environment(data)
		assert str(execinfo.value) == "'Environment' is missing mandatory attribute 'name'"

	def test_shall_raise_exception_when_value_is_not_configured(self):

		data = {
			'condition': "False",
			'name': "CCACHE",
			'description': "Default cache tool for the build toolchain"
		}

		with pytest.raises(MandatoryConfigAttributeMissing) as execinfo:
			Environment(data)
		assert str(execinfo.value) == "'Environment' is missing mandatory attribute 'value'"

	def test_shall_raise_exception_when_method_is_invalid(self):

		data = {
			'condition': "True",
			'name': "CCACHE",
			'value': "123",
			'method': 'invalid',
			'description': "Default cache tool for the build toolchain"
		}

		with pytest.raises(InvalidAttribute) as execinfo:
			Environment(data)
		assert str(execinfo.value) == "'Environment.method' is invalid"

	def test_shall_append_on_other_environment(self):

		sourceDict = {
			'condition': "True",
			'name': "CFLAG",
			'value': "1",
			'description': "Text1",
			'method': None
		}

		otherDict = {
			'condition': "True",
			'name': "CFLAG",
			'value': "2",
			'description': "Text1",
			'method': "append"
		}

		resultDict = {
			'condition': "True",
			'name': "CFLAG",
			'value': "1 2",
			'description': None,
			'method': "append"
		}

		source = Environment(sourceDict)
		other = Environment(otherDict)
		result = source + other

		# Pre
		assert_environment_dict_equal(source, sourceDict)
		assert_environment_dict_equal(other, otherDict)

		# Test
		assert_environment_dict_equal(result, resultDict)

		# Post
		assert_environment_dict_equal(source, sourceDict)
		assert_environment_dict_equal(other, otherDict)

	def test_shall_override_on_other_environment(self):

		sourceDict = {
			'condition': "True",
			'name': "CFLAG",
			'value': "1",
			'description': "Text1",
			'method': None
		}

		otherDict = {
			'condition': "True",
			'name': "CFLAG",
			'value': "2",
			'description': "Text1",
			'method': None
		}

		resultDict = {
			'condition': "True",
			'name': "CFLAG",
			'value': "2",
			'description': None,
			'method': None
		}

		source = Environment(sourceDict)
		other = Environment(otherDict)
		result = source + other

		# Pre
		assert_environment_dict_equal(source, sourceDict)
		assert_environment_dict_equal(other, otherDict)

		# Test
		assert_environment_dict_equal(result, resultDict)

		# Post
		assert_environment_dict_equal(source, sourceDict)
		assert_environment_dict_equal(other, otherDict)

	def test_shall_raise_exception_when_adding_different_names_environment(self):

		sourceDict = {
			'condition': True,
			'name': "name1",
			'value': "1",
			'description': "Text1",
			'method': None
		}

		otherDict = {
			'condition': True,
			'name': "name2",
			'value': "2",
			'description': "Text1",
			'method': None
		}

		source = Environment(sourceDict)
		other = Environment(otherDict)

		# Pre
		assert_environment_dict_equal(source, sourceDict)
		assert_environment_dict_equal(other, otherDict)

		# Test
		with pytest.raises(OperationOnIncompatibleConfigs) as execinfo:
			source + other
		assert str(execinfo.value) == f"Trying to add '{source.name}' + '{other.name}' environment variables"

		# Post
		assert_environment_dict_equal(source, sourceDict)
		assert_environment_dict_equal(other, otherDict)
