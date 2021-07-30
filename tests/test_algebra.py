import unittest
from tools37.algebra import *


class TestAlgebra(unittest.TestCase):
    def test_add(self):
        p1 = Polynom(1, 2, 3)
        p2 = Polynom(2, 3)
        self.assertEqual(p1 + 5, Polynom(6, 2, 3))
        self.assertEqual(p1 + p2, Polynom(3, 5, 3))

    def test_sub(self):
        p1 = Polynom(1, 2, 3)
        p2 = Polynom(2, 3)
        self.assertEqual(p1 - 5, Polynom(-4, 2, 3))
        self.assertEqual(p1 - p2, Polynom(-1, -1, 3))

    def test_mul(self):
        p1 = Polynom(1, 2, 3)
        p2 = Polynom(2, 3)
        self.assertEqual(p1 * 5, Polynom(5, 10, 15))
        self.assertEqual(p1 * p2, Polynom(2, 7, 12, 9))


if __name__ == '__main__':
    unittest.main()
