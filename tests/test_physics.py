import unittest

from tools37.geom import Vector
from tools37.physics import *


class TestPhysic(unittest.TestCase):
    def test_001(self):
        C = Circle(position=Vector(0, 0), radius=1, speed=Vector(1, 0), mass=1)
        L = Line(origin=Vector(10, -1), target=Vector(10, 1), speed=Vector(0, 0), mass=float('inf'))
        self.assertEqual(list(circle_line_collision(C, L)), [(9.0, Vector(-1.0, 0.0)), (11.0, Vector(1.0, 0.0))])

        C = Circle(position=Vector(0, 0), radius=1, speed=Vector(0, 1), mass=1)
        L = Line(origin=Vector(-1, 10), target=Vector(1, 10), speed=Vector(0, 0), mass=float('inf'))
        self.assertEqual(list(circle_line_collision(C, L)), [(9.0, Vector(0.0, -1.0)), (11.0, Vector(0.0, 1.0))])

        C = Circle(position=Vector(0, 0), radius=1, speed=Vector(-1, 0), mass=1)
        L = Line(origin=Vector(-10, -1), target=Vector(-10, 1), speed=Vector(0, 0), mass=float('inf'))
        self.assertEqual(list(circle_line_collision(C, L)), [(9.0, Vector(1.0, 0.0)), (11.0, Vector(-1.0, 0.0))])

        C = Circle(position=Vector(0, 0), radius=1, speed=Vector(0, -1), mass=1)
        L = Line(origin=Vector(-1, -10), target=Vector(1, -10), speed=Vector(0, 0), mass=float('inf'))
        self.assertEqual(list(circle_line_collision(C, L)), [(9.0, Vector(0.0, 1.0)), (11.0, Vector(0.0, -1.0))])

    def test_002(self):
        C1 = Circle(position=Vector(0, 0), radius=1, speed=Vector(1, 0), mass=1)
        C2 = Circle(position=Vector(10, 0), radius=1, speed=Vector(0, 0), mass=1)
        self.assertEqual(list(circle_circle_collision(C1, C2)), [(8.0, Vector(-2.0, 0.0)), (12.0, Vector(2.0, 0.0))])

        C1 = Circle(position=Vector(0, 0), radius=1, speed=Vector(-1, 0), mass=1)
        C2 = Circle(position=Vector(-10, 0), radius=1, speed=Vector(0, 0), mass=1)
        self.assertEqual(list(circle_circle_collision(C1, C2)), [(8.0, Vector(2.0, 0.0)), (12.0, Vector(-2.0, 0.0))])

        C1 = Circle(position=Vector(0, 0), radius=1, speed=Vector(0, 1), mass=1)
        C2 = Circle(position=Vector(0, 10), radius=1, speed=Vector(0, 0), mass=1)
        self.assertEqual(list(circle_circle_collision(C1, C2)), [(8.0, Vector(0.0, -2.0)), (12.0, Vector(0.0, 2.0))])

        C1 = Circle(position=Vector(0, 0), radius=1, speed=Vector(0, -1), mass=1)
        C2 = Circle(position=Vector(0, -10), radius=1, speed=Vector(0, 0), mass=1)
        self.assertEqual(list(circle_circle_collision(C1, C2)), [(8.0, Vector(0.0, 2.0)), (12.0, Vector(0.0, -2.0))])

    def test_003(self):
        for v1, m1, v2, m2, r1, r2 in [
            (5, 1, -5, 1, -5, 5),
            (0, float('inf'), 8, 1, 0, -8),
            (8, 1, 0, float('inf'), -8, 0),
        ]:
            self.assertEqual(elastic_collision(v1, m1, v2, m2), (r1, r2))


if __name__ == '__main__':
    unittest.main()
