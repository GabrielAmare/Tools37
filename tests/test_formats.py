import unittest
from math import isnan

from tools37 import formats as f


class TestFormats(unittest.TestCase):
    def check_parse_equal(self, field: f.Format, input_value, output_value, msg: str = ''):
        self.assertEqual(field.parse(input_value), output_value, msg=msg)

    def check_parse_error(self, field: f.Format, input_value):
        self.assertRaises(f.ParsingError, field.parse, input_value)

    def check_parse_apply(self, field: f.Format, input_value, test_function):
        self.assertTrue(test_function(field.parse(input_value)))

    def test_Integer(self):
        field = f.Integer()

        self.check_parse_equal(field, 0, 0)
        self.check_parse_equal(field, 0.0, 0)
        self.check_parse_equal(field, "0", 0)

        self.check_parse_error(field, 0.1)
        self.check_parse_error(field, "0.0")
        self.check_parse_error(field, "0.1")
        self.check_parse_error(field, "xyz")

    def test_Decimal(self):
        field = f.Decimal()

        self.check_parse_equal(field, 0, 0.0)
        self.check_parse_equal(field, 0.0, 0.0)
        self.check_parse_equal(field, 0.5, 0.5)
        self.check_parse_equal(field, "0", 0.0)
        self.check_parse_equal(field, "0.0", 0.0)
        self.check_parse_equal(field, "inf", float('inf'))
        self.check_parse_equal(field, "-inf", float('-inf'))
        self.check_parse_equal(field, False, 0.0)
        self.check_parse_equal(field, True, 1.0)

        self.check_parse_apply(field, 'nan', isnan)

        self.check_parse_error(field, "0.0.0")
        self.check_parse_error(field, "xyz")

    def test_Boolean(self):
        field = f.Boolean()

        self.check_parse_equal(field, False, False)
        self.check_parse_equal(field, True, True)
        self.check_parse_equal(field, 0, False)
        self.check_parse_equal(field, 1, True)
        self.check_parse_equal(field, 0.0, False)
        self.check_parse_equal(field, 1.0, True)
        self.check_parse_equal(field, "False", False)
        self.check_parse_equal(field, "True", True)

        self.check_parse_error(field, 0.1)
        self.check_parse_error(field, "0.0")
        self.check_parse_error(field, "0.1")
        self.check_parse_error(field, "xyz")

    def test_String(self):
        field = f.String()

        self.check_parse_equal(field, "0", "0")
        self.check_parse_equal(field, 0, "0")
        self.check_parse_equal(field, 0.0, "0.0")
        self.check_parse_equal(field, False, "False")
        self.check_parse_equal(field, True, "True")

    # TODO : write tests for f.Date
    def test_Date(self):
        ...

    # TODO : write tests for f.Datetime
    def test_Datetime(self):
        ...

    # TODO : write tests for f.List
    def test_List(self):
        ...

    # TODO : write tests for f.Tuple
    def test_Tuple(self):
        ...

    # TODO : write tests for f.Dict
    def test_Dict(self):
        ...

    # TODO : write tests for f.Union
    def test_Union(self):
        ...


if __name__ == '__main__':
    unittest.main()
