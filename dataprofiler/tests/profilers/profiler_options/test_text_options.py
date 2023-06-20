pass
import json

from dataprofiler.profilers.json_encoder import ProfileEncoder
from dataprofiler.profilers.profiler_options import TextOptions
from dataprofiler.tests.profilers.profiler_options.test_numerical_options import (
    TestNumericalOptions,
)


class TestTextOptions(TestNumericalOptions):

    option_class = TextOptions
    keys = TestNumericalOptions.keys + ["vocab"]
    numeric_keys = TestNumericalOptions.numeric_keys.copy()
    numeric_keys.remove("num_zeros")
    numeric_keys.remove("num_negatives")

    def test_init(self):
        super().test_init()

    def test_set_helper(self):
        super().test_set_helper()

    def test_set(self):
        super().test_set()

    def test_validate_helper(self):
        super().test_validate_helper()
        options = self.get_options()
        optpth = self.get_options_path()

        # Check to make sure num_zeros/num_negatives is False as a TextOption
        for key in ["num_zeros", "num_negatives"]:
            skey = f"{key}.is_enabled"
            expected_error = (
                "{}.{} should always be disabled, "
                "{}.is_enabled = False".format(optpth, key, key)
            )
            default_bool = options.properties[key].is_enabled
            options.set({skey: True})
            self.assertEqual([expected_error], options._validate_helper())
            options.set({skey: default_bool})

    def test_validate(self):
        super().test_validate()

    def test_is_numeric_stats_enabled(self):
        super().test_is_numeric_stats_enabled()

        options = self.get_options()

        # Disable All Numeric Stats but cheeck num_zeros and num_negatives
        # will not affect is_numeric_stats_enabled
        options.set({f"{key}.is_enabled": False for key in self.numeric_keys})
        options.set({"num_zeros.is_enabled": True})
        self.assertFalse(options.is_numeric_stats_enabled)
        options.set({"num_negatives.is_enabled": True})
        self.assertFalse(options.is_numeric_stats_enabled)

        # Make sure these two variables cannot be influenced by
        # changing is_numeric_stats_enabled
        options.is_numeric_stats_enabled = False
        self.assertTrue(options.num_zeros.is_enabled)
        self.assertTrue(options.num_negatives.is_enabled)

    def test_eq(self):
        super().test_eq()

        options = self.get_options()
        options2 = self.get_options()
        options.vocab.is_enabled = False
        self.assertNotEqual(options, options2)
        options2.vocab.is_enabled = False
        self.assertEqual(options, options2)

    def test_json_encode(self):
        option = TextOptions()

        serialized = json.dumps(option, cls=ProfileEncoder)

        expected_class = "TextOptions"
        expected_options_attributes = {
            "is_enabled",
            "min",
            "max",
            "mode",
            "median",
            "sum",
            "variance",
            "skewness",
            "kurtosis",
            "median_abs_deviation",
            "num_zeros",
            "num_negatives",
            "histogram_and_quantiles",
            "bias_correction",
            "vocab",
        }

        actual_option_json = json.loads(serialized)

        self.assertIn("class", actual_option_json)
        self.assertEqual(expected_class, actual_option_json["class"])
        self.assertIn("data", actual_option_json)
        self.assertEqual(
            expected_options_attributes, set(actual_option_json["data"].keys())
        )
