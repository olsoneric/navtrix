import unittest

from pedemath.quat import Quat
from pedemath.vec3 import Vec3

from navtrix.transform import Transform


class TransformTestCase(unittest.TestCase):
    def test_constructor_no_args(self):
        t = Transform()
        self.assertEqual(t.pos, Vec3(0, 0, 0))
        self.assertEqual(t.rot, Quat())

    def test_constructor_with_args(self):
        t = Transform(Vec3(1, 2, 3), Quat(1, 1, 1, 1))
        self.assertEqual(t.pos, Vec3(1, 2, 3))
        self.assertEqual(t.rot, Quat(1, 1, 1, 1))

    def test_transform_point_in_place_no_rot(self):
        t = Transform(Vec3(1, 2, 3))
        point = Vec3(0, 0, -1)
        t.transform_point_in_place(point)
        self.assertEqual(point, Vec3(1, 2, 2))

    def test_transform_point_in_place_no_translation(self):
        t = Transform(Vec3(0, 0, 0), Quat.from_axis_angle(Vec3(0, 1, 0), 90))
        point = Vec3(0, 0, -1)
        t.transform_point_in_place(point)
        self.assertEqual(point.x, -1)
        self.assertEqual(point.y, 0)
        self.assertAlmostEqual(point.z, 0)

    def test_transform_point_in_place(self):
        t = Transform(Vec3(1, 2, 3), Quat.from_axis_angle(Vec3(0, 1, 0), 90))
        point = Vec3(0, 0, -1)
        t.transform_point_in_place(point)
        self.assertEqual(point, Vec3(0, 2, 3))

    def test_transform(self):
        rot1 = Quat.from_axis_angle(Vec3(0, 1, 0), 90)
        rot2 = Quat.from_axis_angle(Vec3(1, 0, 0), 90)
        t = Transform(Vec3(1, 2, 3), rot1)
        t2 = Transform(Vec3(1, 0, 0), rot2)

        result = t.transform(t2)
        self.assertEqual(result.pos, Vec3(2, 2, 3))  # (0, 1, 0) + (1, 2, 3)
        self.assertEqual(result.rot, rot2 * rot1)
