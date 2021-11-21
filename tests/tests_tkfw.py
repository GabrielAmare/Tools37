import unittest

from tools37.tkfw.evaluable import EvaluableDictItem, EvaluableListItem, EvaluablePath


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


class TestEvaluablePath(unittest.TestCase):
    def test_method_evaluate(self):
        # on wrong type 1
        path = EvaluablePath(steps=[EvaluableDictItem("key"), EvaluableListItem(0)])
        self.assertRaises(TypeError, path.evaluate, data=[])

        # on missing key 1
        path = EvaluablePath(steps=[EvaluableDictItem("key"), EvaluableListItem(0)])
        self.assertRaises(KeyError, path.evaluate, data={})

        # on wrong type 2
        path = EvaluablePath(steps=[EvaluableDictItem("key"), EvaluableListItem(0)])
        self.assertRaises(TypeError, path.evaluate, data={"key": {}})

        # on missing index 2
        path = EvaluablePath(steps=[EvaluableDictItem("key"), EvaluableListItem(0)])
        self.assertRaises(IndexError, path.evaluate, data={"key": []})

        # standard behaviour
        path = EvaluablePath(steps=[EvaluableDictItem("key"), EvaluableListItem(0)])
        self.assertEqual("value", path.evaluate(data={"key": ["value"]}))

    def test_method_get(self):
        # on wrong type 1
        path = EvaluablePath(steps=[EvaluableDictItem("key"), EvaluableListItem(0)])
        self.assertRaises(TypeError, path.get, data=[])

        # on missing key 1
        path = EvaluablePath(steps=[EvaluableDictItem("key"), EvaluableListItem(0)])
        self.assertRaises(KeyError, path.get, data={})

        # on wrong type 2
        path = EvaluablePath(steps=[EvaluableDictItem("key"), EvaluableListItem(0)])
        self.assertRaises(TypeError, path.get, data={"key": {}})

        # on missing index 2
        path = EvaluablePath(steps=[EvaluableDictItem("key"), EvaluableListItem(0)])
        self.assertRaises(IndexError, path.get, data={"key": []})

        # standard behaviour
        path = EvaluablePath(steps=[EvaluableDictItem("key"), EvaluableListItem(0)])
        self.assertEqual("value", path.get(data={"key": ["value"]}))

    def test_method_set(self):
        # on wrong type 1
        path = EvaluablePath(steps=[EvaluableDictItem("key"), EvaluableListItem(0)])
        self.assertRaises(TypeError, path.set, data=[], value=None)

        # on missing key 1
        path = EvaluablePath(steps=[EvaluableDictItem("key"), EvaluableListItem(0)])
        self.assertRaises(KeyError, path.set, data={}, value=None)

        # on wrong type 2
        path = EvaluablePath(steps=[EvaluableDictItem("key"), EvaluableListItem(0)])
        self.assertRaises(TypeError, path.set, data={"key": {}}, value=None)

        # on missing index 2
        path = EvaluablePath(steps=[EvaluableDictItem("key"), EvaluableListItem(0)])
        self.assertRaises(IndexError, path.set, data={"key": []}, value=None)

        # standard behaviour
        path = EvaluablePath(steps=[EvaluableDictItem("key"), EvaluableListItem(0)])
        data = {"key": ["value"]}
        path.set(data=data, value="modified")
        self.assertEqual("modified", data["key"][0])

    def test_dunder_str(self):
        # standard behaviour
        self.assertEqual("key.0", str(EvaluablePath(steps=[EvaluableDictItem("key"), EvaluableListItem(0)])))

    def test_dunder_add(self):
        left = EvaluablePath(steps=[EvaluableDictItem("key")])
        right = EvaluablePath(steps=[EvaluableListItem(0)])

        # standard behaviour
        self.assertEqual(EvaluablePath(steps=left.steps + right.steps), left + right)

    if __name__ == '__main__':
        unittest.main()
