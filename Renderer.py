import Field, pygame, sys
from Point import *

class Renderer(object):
    def __init__(self, width = 640, height = 480):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.field = Field.Field()
        self.field.loadFile("fieldInit.txt")
        self.cameraPoint = Point(width / 2, height / 2, 4)
        self.points = self._generatePoints()

    def draw(self):
        self.screen.fill((0, 0, 0)) 
        for point in self.points:
            planePoint = point.projectTo2D(self.cameraPoint, \
                        self.field.depth)
            pygame.draw.line(self.screen, (255,255,255), \
                    planePoint, (planePoint[0]+1, planePoint[1]))
        pygame.display.flip()

    # mapping field array to world coordinates does not work
    def _generatePoints(self):
        retPoints = []
        width = self.screen.get_width()
        height = self.screen.get_height()
        wMargin = width / 8 
        hMargin = height / 8
        wCell = (width - wMargin * 2) / self.field.width
        hCell = (height- hMargin * 2) / self.field.height
        for z in range(0, self.field.depth):
            for y in range(0, self.field.height):
                for x in range(0, self.field.width):
                    if (self.field.field[z][y][x] == 0):
                        continue
                    tmpPoints = []
                    for pz in range(0, 2):
                        for py in range(0, 2):
                            for px in range(0, 2):
                                xLoc = (x + px) * wCell + wMargin \
                                        - self.cameraPoint.x
                                yLoc = (y + py) * hCell + hMargin \
                                        - self.cameraPoint.y
                                zLoc = (z + pz)
                                point = Point(xLoc, yLoc, zLoc)
                                tmpPoints.append(point)
                    for ele, i in zip(tmpPoints, range(0, len(tmpPoints))):
                        neighDir = []
                        tmp = i
                        if tmp % 2 == 0:
                            neighDir.append(1)
                        else:
                            neighDir.append(-1)
                        if tmp / 4 == 0:
                            neighDir.append(4)
                        else:
                            tmp -= 4
                            neighDir.append(-4)
                        if tmp / 2 == 0:
                            neighDir.append(2)
                        else:
                            neighDir.append(-2)
                        for num in neighDir:
                            ele.neighbours.append(tmpPoints[i + num])
                    retPoints.extend(tmpPoints)
                    tmpPoints = []
        return retPoints

if __name__ == "__main__":
    renderer = Renderer()
    for point in renderer.points:
        print point.x, point.y, point.z
    renderer.draw()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
