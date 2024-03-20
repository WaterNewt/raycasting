import math


class Ray:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.intersecting_walls = []

    def cast(self, walls):
        record = float('inf')
        closest = None

        for wall in walls:
            x1, y1 = wall.start
            x2, y2 = wall.end

            x3, y3 = self.start
            x4, y4 = self.end

            den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

            if den == 0:
                intersecting = False
            else:
                try:
                    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
                    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
                except ZeroDivisionError:
                    t = 0
                    u = 0

                intersecting = 0 < t < 1 and u > 0

                if intersecting:
                    self.intersecting_walls.append(wall)
                    px, py = x1 + t * (x2 - x1), y1 + t * (y2 - y1)
                    d = self.point_dist(px, py)
                    if d < record:
                        record = d
                        closest = (px, py)

        return closest

    def point_dist(self, px, py):
        return math.sqrt((self.start[0] - px) ** 2 + (self.start[1] - py) ** 2)
