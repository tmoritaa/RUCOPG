from numpy import *

class Field(object):

    def __init__(self, width = 0, height = 0, depth = 0):
        self.width = width
        self.height = height
        self.depth = depth
        self._initField()
        self.gravMatrix = array([0, 1, 0])
        self.ROT_XPOS = array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
        self.ROT_XNEG = array([[1, 0, 0], [0, 0, 1], [0, -1, 0]])
        self.ROT_ZPOS = array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
        self.ROT_ZNEG = array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]])

    def _initField(self):
        self.field = []
        self.field = [[[0 for z in range(0, self.width)] \
                for y in range(0, self.height)] \
                for x in range(0, self.depth)]

    def rotate(self, s_dir):
        if (s_dir == "left"):
            self.gravMatrix = dot(self.gravMatrix, self.ROT_XNEG)
        elif (s_dir == "right"):
            self.gravMatrix = dot(self.gravMatrix, self.ROT_XPOS)
        elif (s_dir == "forward"):
            self.gravMatrix = dot(self.gravMatrix, self.ROT_ZPOS)
        elif (s_dir == "back"):
            self.gravMatrix = dot(self.gravMatrix, self.ROT_ZNEG)
        else:
            print "rotation function given invalid direction"

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
        elif plane == "y" or plane == "-y":
            if loc >= self.depth * self.width:
                print "Invalid location index"
                return
            x = loc % self.width
            z = loc / self.width
            yVec = 1 if (plane == "y") else -1
            self._pushYPlaneBlock(yVec, x, z)
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

    def _pushYPlaneBlock(self, yVec, x, z):
        y = (self.height - 1) if (yVec == 1) else 0

        # no block to push
        if self.field[z][y][x] == 0:
            return

        y = (self.height - 2) if (yVec == -1) else 1
        
        while (y >= 0 and y < self.height):
            if self.field[z][y][x] != 0 and self.field[z][y-yVec][x] == 0:
                self.field[z][y-yVec][x] = self.field[z][y][x]
                self.field[z][y][x] = 0
            y += yVec

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

    def loadFile(self, fileName):
        f = open(fileName, 'r')
        s = f.readline().strip()
        self.width = int(s)
        s = f.readline().strip()
        self.height = int(s)
        s = f.readline().strip()
        self.depth = int(s)
        self._initField()
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
    field.pushBlock("y", 3)
    field.formatPrint()
