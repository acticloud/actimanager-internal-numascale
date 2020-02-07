import Servernode
import Socket
import Numanode
import Core

#This class sets up the system model.
#TODO: change to read system config from xml file or similar

class SysDescr(object):

    totalCores = 0
#AC-machines system info
    def __init__(self):
        self.servernodes = []
        noOfServers = 1
        noOfSockets = 4
        noOfNumanodes = 1
        noOfCores = 8
        nodeCounter = 0
        coreCounter = 0

        for m in range(noOfServers):
            snode = Servernode.Servernode(m)
            for n in range(noOfSockets):
                socket = Socket.Socket(n)
                for o in range(noOfNumanodes):
                    node = Numanode.Numanode(nodeCounter)
                    nodeCounter += 1
                    for p in range(noOfCores):
                        core = Core.Core(coreCounter)
                        coreCounter += 1
                        node.addCore(core)
                    socket.addNumanode(node)
                snode.addSocket(socket)
            self.servernodes.append(snode)
        self.totalCores = coreCounter+1

    def getNodeByID(self, ID):
        for sn in self.servernodes:
            for s in sn.sockets:
                for n in s.numanodes:
                    if n.ID == ID:
                        return n

    def getNodeByCoreID(self, ID):
        for sn in self.servernodes:
            for s in sn.sockets:
                for n in s.numanodes:
                    for c in n.cores:
                        if c.ID == ID:
                            return n

    def printMe(self):
        print "Servers: "
        for s in self.servernodes:
            print ("Server ID: "+str(s.ID))
            for k in s.sockets:
                print("Socket: ")+str(k.ID)
                for n in k.numanodes:
                    print("Numanode: "+str(n.ID))
                    for c in n.cores:
                        print ("Core: "+str(c.ID)),
                    print("")
                print("")


#Numascale system info
    # def __init__(self):
    #     self.servernodes = []
    #     noOfServers = 6
    #     noOfSockets = 3
    #     noOfNumanodes = 2
    #     noOfCores = 8
    #     nodeCounter = 0
    #     coreCounter = 0
    #
    #     for m in range(noOfServers):
    #         snode = Servernode.Servernode(m)
    #         for n in range(noOfSockets):
    #             socket = Socket.Socket(n)
    #             for o in range(noOfNumanodes):
    #                 node = Numanode.Numanode(nodeCounter)
    #                 nodeCounter += 1
    #                 for p in range(noOfCores):
    #                     core = Core.Core(coreCounter)
    #                     coreCounter += 1
    #                     node.addCore(core)
    #                 socket.addNumanode(node)
    #             snode.addSocket(socket)
    #         self.servernodes.append(snode)
    #     self.totalCores = coreCounter+1
    #
    # def getNodeByID(self, ID):
    #     for sn in self.servernodes:
    #         for s in sn.sockets:
    #             for n in s.numanodes:
    #                 if n.ID == ID:
    #                     return n
    #
    # def getNodeByCoreID(self, ID):
    #     for sn in self.servernodes:
    #         for s in sn.sockets:
    #             for n in s.numanodes:
    #                 for c in n.cores:
    #                     if c.ID == ID:
    #                         return n
    #
    # def printMe(self):
    #     print "Servers: "
    #     for s in self.servernodes:
    #         print ("Server ID: "+str(s.ID))
    #         for k in s.sockets:
    #             print("Socket: ")+str(k.ID)
    #             for n in k.numanodes:
    #                 print("Numanode: "+str(n.ID))
    #                 for c in n.cores:
    #                     print ("Core: "+str(c.ID)),
    #                 print("")
    #             print("")
