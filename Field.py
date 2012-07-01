from numpy import *

class Field(object):

    def __init__(self, width = 0, height = 0, depth = 0):
        self.field = [[[0 for z in range(0, depth)] \
                for y in range(0, height)] \
                for x in range(0, width)]
        self.gravMatrix = array([0, 1, 0])
        self.ROT_XPOS = array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
        self.ROT_XNEG = array([[1, 0, 0], [0, 0, 1], [0, -1, 0]])
        self.ROT_ZPOS = array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
        self.ROT_ZNEG = array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]])

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
        

if __name__ == "__main__":
    field = Field(2, 2, 2)
