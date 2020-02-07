import subprocess
from subprocess import check_output
class Numa(object):

    def __init__(self):
        self.numServers=6
        self.numaSize=32768.0 #in MB
        self.runCommand()


    def runCommand(self):

        output = check_output ("numactl --show", shell = True, stderr=subprocess.STDOUT)

        lines = output.splitlines()
        for line in lines:
            if "physcpubind:" in line:
                self.cores = len((line.strip()).split(" "))-1
            elif "cpubind:" in line:
                self.nodes = len((line.strip()).split(" "))-1

       ##return the least core id  for the given node
    def getStartOfCoreNodeN(self, node):
        return int(self.cores/self.nodes)*node

    ##return the least core id  for the given server
    def getStartOfCoreServerS(self, server):
        return int(self.cores / self.numServers) * server

    def getCoresPerNode(self):
        return int(self.cores / (self.nodes*self.numServers))

    def getCoresPerServer(self):
        return int(self.cores / self.numServers)

    def getServer(self,node):
        return int(node)/self.numServers

    def getNumaPerserver(self):
        return self.nodes/self.numServers


    def getNumaSize(self):
        return self.numaSize

    def getNodes(self):
        return self.nodes

    def isInServer(self, core, node):
        if int(node/self.getNumaPerserver())== int(core/self.getCoresPerServer()):
            return True
        else:
            return False

    def getCoresInServer(self, server):
        cores =[]
        startIndex= self.getStartOfCoreServerS(server)
        coresInServer=self.getCoresPerServer()
        for i in range(startIndex,startIndex+coresInServer):
            cores.append(i)

        return cores

    def getCoresInNUMANode(self, node):
        cores =[]
        startIndex= self.getStartOfCoreNodeN(node)
        coresInNode=self.getCoresPerNode()
        for i in range(startIndex,startIndex+coresInNode):
            cores.append(i)

        return cores

    #given the core, returns the node where the core is belongs
    def getNodeForCore(self,core):
        return core % self.getCoresPerNode()






#print Numa.getStartOfCore(0)