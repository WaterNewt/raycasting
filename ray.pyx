import math

cdef class Ray:
    cdef tuple start
    cdef tuple end
    cdef list intersecting_walls

    def __cinit__(self, start, end):
        """
        Initialize the ray line
        :param start: The start position of the ray line
        :param end: The end position of the ray line
        """
        self.start = start
        self.end = end
        self.intersecting_walls = []

    cpdef cast(self, walls):
        """
        Cast the rays to the walls and check for intersection
        :param walls: The walls for the ray to cast
        :return: Returns position of the closest intersection. Returns None, if no intersection
        """
        cdef float record = float('inf')
        cdef tuple closest = None

        cdef float x1, y1, x2, y2, x3, y3, x4, y4
        cdef float den, t, u, px, py, d
        cdef bint intersecting

        for wall in walls:
            wall.intersecting = False
            x1, y1 = wall.start
            x2, y2 = wall.end

            x3, y3 = self.start
            x4, y4 = self.end

            den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

            if den != 0:
                try:
                    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
                    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
                except ZeroDivisionError:
                    t = 0
                    u = 0

                intersecting = 0 < t < 1 and u > 0

                if intersecting:
                    wall.intersecting = True
                    self.intersecting_walls.append(wall)
                    px, py = x1 + t * (x2 - x1), y1 + t * (y2 - y1)
                    d = self.point_dist(px, py)
                    if d < record:
                        record = d
                        closest = (px, py)

        return closest

    cpdef point_dist(self, float px, float py):
        """
        Distance between two points
        :param px: The x point
        :param py: The y point
        :return: Returns the distance
        """
        return math.sqrt((self.start[0] - px) ** 2 + (self.start[1] - py) ** 2)
