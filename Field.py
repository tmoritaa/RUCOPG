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


if __name__ == "__main__":
    field = Field(4, 3, 2)
    field.loadFile("fieldInit.txt")
    field.formatPrint()
