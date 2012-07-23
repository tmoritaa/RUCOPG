import math

class Point(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.neighbours = []

    def projectTo2D(self, camera, fieldDepth):
        # currently does not take into account rotation
        zRatio = 1.0 / (fieldDepth + 2.0)
        factor = 1.0 - zRatio * (fieldDepth - math.fabs(self.z))
        dx = float(self.x) * factor + camera.x
        dy = float(self.y) * factor + camera.y
        print "dx, dy", dx, dy
        return (dx, dy)
