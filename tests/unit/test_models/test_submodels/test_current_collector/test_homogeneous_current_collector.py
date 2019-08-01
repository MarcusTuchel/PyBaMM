#
# Test uniform current collector submodel
#

import pybamm
import tests
import unittest


class TestUniformModel(unittest.TestCase):
    def test_public_functions(self):
        param = pybamm.standard_parameters_lithium_ion

        submodel = pybamm.current_collector.Uniform(param)
        variables = {"Local current collector potential difference": pybamm.Scalar(0)}
        std_tests = tests.StandardSubModelTests(submodel, variables)
        std_tests.test_all()


if __name__ == "__main__":
    print("Add -v for more debug output")
    import sys

    if "-v" in sys.argv:
        debug = True
    pybamm.settings.debug_mode = True
    unittest.main()
