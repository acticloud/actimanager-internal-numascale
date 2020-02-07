import Numadistance
import Core

class Numanode(object):

    def __init__(self, ID):
       self.ID = ID
       self.cores = []

    def getDistance(self, node2):
       ndistance = Numadistance.Numadistance()
       return ndistance.getNumaDistance(self.ID, node2.ID)

    def addCore(self, core):
       self.cores.append(core)