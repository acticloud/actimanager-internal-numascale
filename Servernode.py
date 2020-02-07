#import Socket

class Servernode(object):

    def __init__(self, ID):
        self.ID=ID
        self.sockets = []

    def addSocket(self, socket):
       self.sockets.append(socket)

    def removeSocket(self, socket):
       self.sockets.remove(socket)

    def printMe(self):
       print "Servernode: " + str(self.ID)
       print("Sockets: "),
       for s in self.sockets:
           print(" " + str(s.ID))

