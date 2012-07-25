import Field, pygame, sys
from Point import *

class Face(object):
    def __init__(self, _points, _leastDepth):
        self.pointIds = _points
        self.leastDepth = _leastDepth

class Renderer(object):
    def __init__(self, width = 640, height = 480):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.field = Field.Field()
        self.field.loadFile("fieldInit.txt")
        self.cameraPoint = Point(width / 2, height / 2, 4)
        self.points = self._generatePoints()
        self.faces = self._generateFaces()

    def draw(self):
        self.screen.fill((0, 0, 0)) 
        for face in self.faces:
            print "depth", face.leastDepth
            pointList = []
            for num in face.pointIds:
                point = self.points[num]
                point = point.projectTo2D(self.cameraPoint, self.field.depth)
                pointList.append(point)
            pygame.draw.polygon(self.screen, (255, 255, 255), \
                    (pointList[0], pointList[1], pointList[2], pointList[3]))
            for i in range(4):
                j = (i + 1) % 4
                pygame.draw.line(self.screen, (255,0,0), \
                        pointList[i], pointList[j])
        pygame.display.flip()

    def _generatePoints(self):
        retPoints = []
        width = self.screen.get_width()
        height = self.screen.get_height()
        wMargin = width / 8 
        hMargin = height / 8
        wCell = (width - wMargin * 2) / self.field.width
        hCell = (height- hMargin * 2) / self.field.height
        for z in range(self.field.depth):
            for y in range(self.field.height):
                for x in range(self.field.width):
                    if (self.field.field[z][y][x] == 0):
                        continue
                    for pz in range(2):
                        for py in range(2):
                            for px in range(2):
                                xLoc = (x + px) * wCell + wMargin \
                                        - self.cameraPoint.x
                                yLoc = (y + py) * hCell + hMargin \
                                        - self.cameraPoint.y
                                zLoc = (z + pz)
                                point = Point(xLoc, yLoc, zLoc)
                                retPoints.append(point)
        return retPoints

    # self.points must be already generated
    def _generateFaces(self):
        faceList = []
        additions = [(0, 1, 3, 2), (0, 1, 5, 4), (0, 2, 6, 4), \
                                (4, 5, 7, 6), (1, 3, 7, 5), (2, 3, 7, 6)]
        for i in range(0, len(self.points), 8):
            for tup in additions:
                tmpTup = (i+tup[0], i+tup[1], i+tup[2], i+tup[3])
                depth = self._findLowestDepth(tmpTup)
                face = Face(tmpTup, depth)
                faceList.append(face)
        return faceList

    def _findLowestDepth(self, pointIds):
        leastDepth = 9999
        for i in pointIds:
            if self.points[i].z < leastDepth:
                leastDepth = self.points[i].z
        return leastDepth

if __name__ == "__main__":
    renderer = Renderer()
    for point in renderer.points:
        print point.x, point.y, point.z
    renderer.draw()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
