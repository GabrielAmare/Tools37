import unittest

from tools37.tkfw.evaluable import EvaluableDictItem


class TestEvaluableDictItem(unittest.TestCase):
    def test_method_evaluate(self):
        # on missing key
        self.assertRaises(KeyError, EvaluableDictItem("key").evaluate, {})

        # on wrong data type
        self.assertRaises(TypeError, EvaluableDictItem("key").evaluate, [])

        # standard behaviour
        self.assertEqual("value", EvaluableDictItem("key").evaluate({"key": "value"}))

    def test_method_get(self):
        # on missing key
        self.assertRaises(KeyError, EvaluableDictItem("key").get, {})

        # on wrong data type
        self.assertRaises(TypeError, EvaluableDictItem("key").get, [])

        # standard behaviour
        self.assertEqual("value", EvaluableDictItem("key").get({"key": "value"}))

    def test_method_set(self):
        # standard behaviour : key doesn't exists
        data = {}
        EvaluableDictItem("key").set(data, "value")
        self.assertEqual(data["key"], "value")

        # standard behaviour : key already exists
        data = {"key": "value"}
        EvaluableDictItem("key").set(data, "modified")
        self.assertEqual(data["key"], "modified")


if __name__ == '__main__':
    unittest.main()
