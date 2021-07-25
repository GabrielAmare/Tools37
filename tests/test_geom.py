import random
import unittest

from tools37.geom import *


def generate_vector_list(size: int, x_min: float, x_max: float, y_min: float, y_max: float):
    return [
        Vector(random.uniform(x_min, x_max), random.uniform(y_min, y_max))
        for _ in range(size)
    ]


VECTOR_LIST = generate_vector_list(200, -10, 10, -10, 10)


class TestVector(unittest.TestCase):
    def test_repr(self):
        """Test the __repr__ method. (by using the property eval(repr(obj)) == obj)"""
        for v in VECTOR_LIST:
            self.assertEqual(eval(repr(v)), v)

    def test_abs(self):
        """Check the __abs__ method."""
        v = Vector(3, 4)
        self.assertEqual(abs(v), 5)

    def test_getitem(self):
        """Check the __getitem__ method."""
        v = Vector(2, 3)
        self.assertEqual(v[0], 2)
        self.assertEqual(v[1], 3)
        self.assertRaises(IndexError, lambda: v[-1])
        self.assertRaises(IndexError, lambda: v[-2])
        self.assertRaises(IndexError, lambda: v[2])

    def test_setitem(self):
        """Check the __setitem__ method."""
        v = Vector(5, 6)
        v[0] = 2
        v[1] = 3
        self.assertEqual(v[0], 2)
        self.assertEqual(v[1], 3)

    def test_add(self):
        """Check the __add__ method."""
        ex = Vector(1, 0)
        ey = Vector(0, 1)

        self.assertEqual(ex + ey, Vector(1, 1))
        self.assertEqual(ex + 1, Vector(2, 1))
        self.assertRaises(TypeError, lambda: ex + (2, 5))

    def test_sub(self):
        """Check the __sub__ method."""
        ex = Vector(1, 0)
        ey = Vector(0, 1)

        self.assertEqual(ex - ey, Vector(1, -1))
        self.assertEqual(ex - 1, Vector(0, -1))
        self.assertEqual(1 - ex, Vector(0, 1))
        self.assertRaises(TypeError, lambda: ex - (2, 5))

    def test_mul(self):
        """Check the __mul__ method."""
        ex = Vector(1, 0)
        ey = Vector(0, 1)

        self.assertEqual(ex * ey, 0)
        self.assertEqual(ey * ex, 0)
        self.assertEqual(ex * ex, 1)
        self.assertEqual(ey * ey, 1)
        self.assertEqual(2 * ex, Vector(2, 0))
        self.assertEqual(2 * ey, Vector(0, 2))
        self.assertEqual(ex * 2, Vector(2, 0))
        self.assertEqual(ey * 2, Vector(0, 2))
        self.assertRaises(TypeError, lambda: ex * (0, 2))

    def test_xor(self):
        """Check the __xor__ method."""
        ex = Vector(1, 0)
        ey = Vector(0, 1)

        self.assertEqual(ex ^ ey, 1)
        self.assertEqual(ey ^ ex, -1)
        self.assertEqual(ex ^ ex, 0)
        self.assertEqual(ey ^ ey, 0)
        self.assertRaises(TypeError, lambda: ex ^ 2)

    def test_products(self):
        """
            Check the property of inner and outer product that
            u*v=abs(u)*abs(v)*cos(u,v)
            u^v=abs(u)*abs(v)*sin(u,v)
            by using the cos(a)**2 + sin(b)**2 == 1
        """
        for u in VECTOR_LIST:
            for v in VECTOR_LIST:
                self.assertAlmostEqual((u * v) ** 2 + (u ^ v) ** 2, abs(u) ** 2 * abs(v) ** 2, 9)


if __name__ == '__main__':
    unittest.main()
