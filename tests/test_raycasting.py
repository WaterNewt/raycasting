import sys
import os
import unittest
os.system("cythonize -i walls.pyx")
os.system("cythonize -i ray.pyx")
sys.path.insert(1, '..')
import ray
import walls


class TestIntersection(unittest.TestCase):
    def setUp(self):
        self.ray = ray.Ray((651, 612), (629, 92))
        self.wall = walls.Wall((268, 356), (1088, 335))

    def test_intersection(self):
        self.ray.cast([self.wall])
        self.assertEqual(len(self.ray.intersecting_walls), 1)


if __name__ == '__main__':
    unittest.main()
