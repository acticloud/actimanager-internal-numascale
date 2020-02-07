import Numanode

class Socket(object):

    def __init__(self, ID):
        self.ID=ID
        self.numanodes = []

    def addNumanode(self, numanode):
        self.numanodes.append(numanode)

    def removeNumanode(self, numanode):
        self.numanodes.remove(numanode)

    def printMe(self):
        print "Socket: " + str(self.ID)
        print("Numanodes: "),
        for n in self.numanodes:
           print(" " + str(n.ID))