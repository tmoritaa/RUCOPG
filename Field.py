from numpy import *

class Field(object):

    def __init__(self, width = 0, height = 0, depth = 0):
        self.width = width
        self.height = height
        self.depth = depth
        self.field = self._initField(self.width, self.height, self.depth)
        self.ROT_XPOS = array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
        self.ROT_XNEG = array([[1, 0, 0], [0, 0, 1], [0, -1, 0]])
        self.ROT_ZPOS = array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
        self.ROT_ZNEG = array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]])

    def _initField(self, width, height, depth):
        field = [[[0 for z in range(0, width)] \
                for y in range(0, height)] \
                for x in range(0, depth)]
        return field

    def rotate(self, s_dir):
        if (s_dir == "back"):
            self._rotateXAxis(self.ROT_XNEG)
        elif (s_dir == "forward"):
            self._rotateXAxis(self.ROT_XPOS)
        elif (s_dir == "right"):
            self._rotateZAxis(self.ROT_ZNEG)
        elif (s_dir == "left"):
            self._rotateZAxis(self.ROT_ZPOS)

    def _rotateXAxis(self, rotMat):
        newHeight = self.depth
        newDepth = self.height
        newField = self._initField(self.width, newHeight, newDepth)

        midY = self.height / 2
        midZ = self.depth / 2 

        for z in range(0, self.depth):
            relZ = float(z - midZ)
            if self.depth % 2 == 0:
                relZ += 0.5
            for y in range(0, self.height):
                relY = float(y - midY)
                if self.height % 2 == 0:
                    relY += 0.5
                for x in range(0, self.width):
                    sqVec = array([x, relY, relZ])
                    sqVec = dot(sqVec, rotMat)
                    newMidHeight = newHeight / 2
                    newMidDepth = newDepth / 2
                    newX = sqVec[0]
                    newY = sqVec[1] + newMidHeight
                    newZ = sqVec[2] + newMidDepth
                    if newHeight % 2 == 0:
                        newY -= 0.5
                    if newDepth % 2 == 0:
                        newZ -= 0.5
                    newField[int(newZ)][int(newY)][int(newX)] = \
                        self.field[z][y][x]
        self.field = []
        self.field = newField
        self.height = newHeight
        self.depth = newDepth

    def _rotateZAxis(self, rotMat):
        newWidth = self.height
        newHeight = self.width
        newField = self._initField(newWidth, newHeight, self.depth)

        midX = self.width/ 2
        midY = self.height / 2 

        for z in range(0, self.depth):
            for y in range(0, self.height):
                relY = float(y - midY)
                if self.height % 2 == 0:
                    relY += 0.5
                for x in range(0, self.width):
                    relX = float(x - midX)
                    if self.width % 2 == 0:
                        relX += 0.5
                    sqVec = array([relX, relY, z])
                    sqVec = dot(sqVec, rotMat)
                    newMidWidth = newWidth / 2
                    newMidHeight = newHeight / 2
                    newX = sqVec[0] + newMidWidth
                    newY = sqVec[1] + newMidHeight
                    newZ = sqVec[2] 
                    if newWidth % 2 == 0:
                        newX -= 0.5
                    if newHeight % 2 == 0:
                        newY -= 0.5
                    newField[int(newZ)][int(newY)][int(newX)] = \
                        self.field[z][y][x]
        self.field = []
        self.field = newField
        self.width= newWidth
        self.height = newHeight

    def pushBlock(self, plane, loc):
        if plane == "z" or plane == "-z":
            if loc >= self.width * self.height:
                print "Invalid location index"
                return
            x = loc % self.width
            y = loc / self.width
            zVec = 1 if (plane == "z") else -1
            self._pushZPlaneBlock(zVec, x, y)
        elif plane == "x" or plane == "-x":
            if loc >= self.depth * self.height:
                print "Invalid location index"
                return
            z = loc % self.depth
            y = loc / self.depth
            xVec = 1 if (plane == "x") else -1
            self._pushXPlaneBlock(xVec, y, z)
        else:
            print "Invalid plane location"

    def _pushXPlaneBlock(self, xVec, y, z):
        x = (self.width - 1) if (xVec == 1) else 0

        # no block to push
        if self.field[z][y][x] == 0:
            return

        x = (self.width - 2) if (xVec == -1) else 1

        while (x >= 0 and x < self.width):
            if self.field[z][y][x] != 0 and self.field[z][y][x-xVec] == 0:
                self.field[z][y][x-xVec] = self.field[z][y][x]
                self.field[z][y][x] = 0
            x += xVec

    def _pushZPlaneBlock(self, zVec, x, y):
        z = (self.depth - 1) if (zVec == 1) else 0

        # no block to push
        if self.field[z][y][x] == 0:
            return

        z = (self.depth - 2) if (zVec == -1) else 1
        
        while (z >= 0 and z < self.depth):
            if self.field[z][y][x] != 0 and self.field[z-zVec][y][x] == 0:
                self.field[z-zVec][y][x] = self.field[z][y][x]
                self.field[z][y][x] = 0
            z += zVec

    def applyGravity(self):
        for z in range(0, self.depth):
            for x in range(0, self.width):
                curIdx = self.height - 1
                prevOpenList = []
                while curIdx < self.height and curIdx >= 0:
                    if self.field[z][curIdx][x] != 0 and len(prevOpenList) != 0:
                        prevOpenIdx = prevOpenList.pop(0)
                        self.field[z][prevOpenIdx][x] = self.field[z][curIdx][x]
                        self.field[z][curIdx][x] = 0
                    if self.field[z][curIdx][x] == 0:
                        prevOpenList.append(curIdx)
                    curIdx -= 1

    def loadFile(self, fileName):
        f = open(fileName, 'r')
        s = f.readline().strip()
        self.width = int(s)
        s = f.readline().strip()
        self.height = int(s)
        s = f.readline().strip()
        self.depth = int(s)
        self.field = self._initField(self.width, self.height, self.depth)
        i = 0
        while i < (self.width * self.height * self.depth):
            s = f.readline().strip()
            l = s.split(' ')
            for ele in l:
                zpos = int(i / (self.width * self.height))
                ypos = int((i % (self.width * self.height)) / (self.width))
                xpos = i % self.width
                self.field[zpos][ypos][xpos] = int(ele)
                i += 1

    def formatPrint(self):
        for z in range(0, self.depth):
            for y in range(0, self.height):
                print self.field[z][y]
            print "-" * (self.width * 5)
        print


if __name__ == "__main__":
    field = Field(4, 3, 2)
    field.loadFile("fieldInit.txt")
    field.formatPrint()
    field.rotate("forward")
    field.formatPrint()
    field.applyGravity()
    field.formatPrint()
