# Enhancements:
# - Generate all possible points, then use indices to represent points and
#   faces for existing cubes in field

import Field, pygame, sys
from Point import *

class Face(object):
    def __init__(self, _points, _minDepth, _maxDepth, _distCen = 0):
        self.pointIds = _points
        self.distCen = _distCen
        self.minDepth = _minDepth
        self.maxDepth = _maxDepth

class Renderer(object):
    def __init__(self, width = 640, height = 480):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.field = Field.Field()
        self.field.loadFile("fieldInit.txt")
        self.cameraPoint = Point(width / 2, height / 2, 0)
        self.setupPrimitives()

    def setupPrimitives(self):
        self.points = []
        self.faces = []
        self._generatePoints()
        self._generateFaces()
        self.faces.sort(key = lambda k: (k.maxDepth, k.minDepth, k.distCen))

    def draw(self):
        self.screen.fill((0, 0, 0)) 
        for face in self.faces:
            pointList = []
            for num in face.pointIds:
                point = self.points[num]
                point = point.projectTo2D(self.cameraPoint, self.field.depth)
                pointList.append(point)
           
            val = 255
            colour = [val, val, val]

            pygame.draw.polygon(self.screen, tuple(colour), \
                    (pointList[0], pointList[1], pointList[2], pointList[3]))
            for i in range(4):
                j = (i + 1) % 4
                pygame.draw.line(self.screen, (255, 0, 0), \
                    pointList[i], pointList[j])

        pygame.display.flip()
        self.field.formatPrint()

    def handleUp(self):
       self.field.rotate("forward")
       self.setupPrimitives()
       self.draw()

    def handleDown(self):
       self.field.rotate("back")
       self.setupPrimitives()
       self.draw()

    def handleLeft(self):
       self.field.rotate("left")
       self.setupPrimitives()
       self.draw()

    def handleRight(self):
       self.field.rotate("right")
       self.setupPrimitives()
       self.draw()

    def _generatePoints(self):
        width = self.screen.get_width()
        height = self.screen.get_height()
        wMargin = width / 8 
        hMargin = height / 8
        wCell = (width - wMargin * 2) / self.field.width
        hCell = (height- hMargin * 2) / self.field.height

        self._generateBorderPoints()

        # generate points of cubes in field
        for z in range(self.field.depth):
            for y in range(self.field.height):
                for x in range(self.field.width):
                    if self.field.field[z][y][x] == 0:
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
                                self.points.append(point)

    def _generateBorderPoints(self):
        width = self.screen.get_width()
        height = self.screen.get_height()
        wMargin = width / 8 
        hMargin = height / 8
        wCell = (width - wMargin * 2) / self.field.width
        hCell = (height- hMargin * 2) / self.field.height

    # self.points must be already generated
    def _generateFaces(self):
        additions = [(0, 1, 3, 2), (0, 1, 5, 4), (0, 2, 6, 4), \
                                (1, 3, 7, 5), (2, 3, 7, 6), (4, 5, 7, 6)]
        # generate cube faces in field
        for i in range(0, len(self.points), 8):
            for tup in additions:
                tmpTup = (i+tup[0], i+tup[1], i+tup[2], i+tup[3])
                depths = self._findMinMaxDepth(tmpTup)
                face = Face(tmpTup, depths[0], depths[1])
                dist = self._calculateDistanceFP(face, self.cameraPoint)
                face.distCen = dist
                self.faces.append(face)

    def _findMinMaxDepth(self, pointIds):
        minVal = 99
        maxVal = -99
        for i in pointIds:
            if self.points[i].z > maxVal:
                maxVal = self.points[i].z
            if self.points[i].z < minVal:
                minVal = self.points[i].z
        return (minVal, maxVal)

    def _calculateDistanceFP(self, f1, p1):
        avgx = 0.0
        avgy = 0.0
        avgz = 0.0
        vertNum = float(len(f1.pointIds))
        for num in f1.pointIds:
            point = self.points[num]
            avgx += math.fabs(point.x)
            avgy += math.fabs(point.y)
            avgz += math.fabs(point.z)
        p2 = Point(avgx / vertNum, avgy / vertNum, avgz / vertNum)
        absx = math.fabs(p1.x - p2.x)
        absy = math.fabs(p1.y - p2.y)
        absz = math.fabs(p1.z - p2.z)
        dist = math.sqrt(absx*absx + absy*absy + absz*absz)
        return dist 
        

if __name__ == "__main__":
    renderer = Renderer()
    renderer.draw()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    renderer.handleUp()
                elif event.key == pygame.K_DOWN:
                    renderer.handleDown()
                elif event.key == pygame.K_LEFT:
                    renderer.handleLeft()
                elif event.key == pygame.K_RIGHT:
                    renderer.handleRight()
                elif event.key == pygame.K_ESCAPE:
                    sys.exit()

