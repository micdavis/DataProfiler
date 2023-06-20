import json

from dataprofiler.profilers.json_encoder import ProfileEncoder
from dataprofiler.profilers.profiler_options import BaseInspectorOptions
from dataprofiler.tests.profilers.profiler_options.test_boolean_option import (
    TestBooleanOption,
)


class TestBaseInspectorOptions(TestBooleanOption):

    option_class = BaseInspectorOptions

    @classmethod
    def get_options(cls, *args, **params):
        cls.validate_option_class()
        options = cls.option_class()
        options.set(params)
        return options

    def test_init(self):
        super().test_init()

    def test_set_helper(self):
        super().test_set_helper()

    def test_set(self):
        super().test_set()

    def test_validate_helper(self):
        super().test_validate_helper()

    def test_validate(self):
        super().test_validate()

    def test_is_prop_enabled(self):
        options = self.get_options()
        optpth = self.get_options_path()

        # Check is prop enabled for valid property
        options.set({"is_enabled": True})
        self.assertTrue(options.is_prop_enabled("is_enabled"))
        options.set({"is_enabled": False})
        self.assertFalse(options.is_prop_enabled("is_enabled"))

        # Check is prop enabled for invalid property
        expected_error = f'Property "Hello World" does not exist in {optpth}.'
        with self.assertRaisesRegex(AttributeError, expected_error):
            options.is_prop_enabled("Hello World")

    def test_eq(self):
        super().test_eq()

    def test_json_encode(self):
        option = BaseInspectorOptions(is_enabled=False)

        serialized = json.dumps(option, cls=ProfileEncoder)

        expected_class = "BaseInspectorOptions"
        expected_options_attributes = {"is_enabled"}
        expected_is_enabled = option.is_enabled

        actual_option_json = json.loads(serialized)

        self.assertEqual(expected_class, actual_option_json["class"])
        self.assertEqual(
            expected_options_attributes, set(actual_option_json["data"].keys())
        )
        self.assertEqual(expected_is_enabled, actual_option_json["data"]["is_enabled"])
