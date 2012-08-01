# Enhancements:
# - Generate all possible points, then use indices to represent points and
#   faces for existing cubes in field

# TODO: Replace draw borders to really only draw borders of field cube

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
        self.points = []
        self.borderPoints = []
        self._generatePoints()
        self.faces = []
        self.borderFaces = []
        self._generateFaces()
        self.faces = sorted(self.faces, key=lambda k: \
                            (k.maxDepth, k.minDepth, k.distCen))
        #self.faces.sort(key = lambda x: x.maxDepth, reverse=True)

    def draw(self):
        self.screen.fill((0, 0, 0)) 
        for face in self.faces:
            pointList = []
            for num in face.pointIds:
                point = self.points[num]
                point = point.projectTo2D(self.cameraPoint, self.field.depth)
                pointList.append(point)
           
            #depth = self.field.depth
            #val = 255 - (depth - face.maxDepth)  * (100 / depth)
            val = 255
            colour = [val, val, val]

            pygame.draw.polygon(self.screen, tuple(colour), \
                    (pointList[0], pointList[1], pointList[2], pointList[3]))
            for i in range(4):
                j = (i + 1) % 4
                pygame.draw.line(self.screen, (255, 0, 0), \
                    pointList[i], pointList[j])

        self._drawBorders()
        pygame.display.flip()

    def _drawBorders(self):
        for face in self.borderFaces:
            pointList = []
            for num in face.pointIds:
                point = self.borderPoints[num]
                point = point.projectTo2D(self.cameraPoint, self.field.depth)
                pointList.append(point)
            for i in range(4):
                j = (i + 1) % 4
                pygame.draw.line(self.screen, (0, 100, 0), \
                    pointList[i], pointList[j])


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

        # generate border points as well 
        # WOH MANUAL AKDSJFKAFDS
        cornerTL = (wMargin - self.cameraPoint.x, hMargin - self.cameraPoint.y)
        cornerBL = (wMargin - self.cameraPoint.x, \
                    height - hMargin - self.cameraPoint.y)
        cornerTR = (width - wMargin - self.cameraPoint.x, \
                    hMargin - self.cameraPoint.y)
        cornerBR = (width - wMargin - self.cameraPoint.x, \
                    height - hMargin - self.cameraPoint.y)
        self.borderPoints.append(Point(cornerTL[0], cornerTL[1], 0))
        self.borderPoints.append(Point(cornerTR[0], cornerTR[1], 0))
        self.borderPoints.append(Point(cornerBL[0], cornerBL[1], 0))
        self.borderPoints.append(Point(cornerBR[0], cornerBR[1], 0))
        self.borderPoints.append(Point(cornerTL[0], cornerTL[1], \
                                        self.field.depth))
        self.borderPoints.append(Point(cornerTR[0], cornerTR[1], \
                                        self.field.depth))
        self.borderPoints.append(Point(cornerBL[0], cornerBL[1], \
                                        self.field.depth))
        self.borderPoints.append(Point(cornerBR[0], cornerBR[1], \
                                        self.field.depth))

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
                if i == 0:
                    self.borderFaces.append(face)

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
            #else if event.type == KEYDOWN:
             #   if event.key == K_
