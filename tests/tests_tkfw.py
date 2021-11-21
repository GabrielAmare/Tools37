import unittest

from tools37.tkfw.evaluable import EvaluableDictItem, EvaluableListItem


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


class TestEvaluableListItem(unittest.TestCase):
    def test_method_evaluate(self):
        # on missing index
        self.assertRaises(IndexError, EvaluableListItem(index=0).evaluate, [])

        # on wrong data type
        self.assertRaises(TypeError, EvaluableListItem(index=0).evaluate, {})

        # standard behaviour
        self.assertEqual("value", EvaluableListItem(index=0).evaluate(["value"]))

    def test_method_get(self):
        # on missing index
        self.assertRaises(IndexError, EvaluableListItem(index=0).get, [])

        # on wrong data type
        self.assertRaises(TypeError, EvaluableListItem(index=0).get, {})

        # standard behaviour
        self.assertEqual("value", EvaluableListItem(index=0).get(["value"]))

    def test_method_set(self):
        # on missing index
        self.assertRaises(IndexError, EvaluableListItem(index=0).set, data=[], value="value")

        # standard behaviour
        data = ["value"]
        EvaluableListItem(index=0).set(data, "modified")
        self.assertEqual(data[0], "modified")


if __name__ == '__main__':
    unittest.main()
