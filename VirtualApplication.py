#import VirtualCpu
import VirtualMachine
from Actuator import Actuator
from Numa import Numa
import VirtualCpu

class VirtualApplication(object):

    def __init__(self, virtualMachine):
        #self.virtualMachine = virtualMachine

        self.memoryNumaNodes = virtualMachine.nodeset  # list of numa nodes for allocated memory
        self.migrate=0
        self.name = virtualMachine.name
        #print ("name:"+ self.name)
        self.domainID = virtualMachine.domain
        self.cpus = []
        self.setCpus(virtualMachine.vCpus)
        self.cores=[]
        #self.servers=[]
        #self.setMemoryNumaNodes(self.memoryNumaNodes)
        self.sockets=[]
        self.memorySize=float(virtualMachine.memorySize)

        #self.numaNodes = [] #list of numa nodes for allocated cores

        self.soloIPC = 0
        self.soloMPI = 0
        self.IPC = 0
        self.MPI = 0
        self.className="" #Devil,Sheep, Rabit
        self.servers=[]
        self.setServers(self.memoryNumaNodes)

    def setClassName(self,name):
        self.className=name

    def getClassName(self):
        return self.className

    def setCpus(self, vCpus):
        self.cpus=vCpus
        self.updateCores()

    def updateCores(self):

        self.cores=[]
        for vcpu in self.cpus:
            self.cores.append(vcpu.affinity)
            #print ("cores" +str(vcpu.affinity))

    def removeCores(self,cores):
        for c in cores:
            for cc in self.cpus:

                if cc.affinity==c:
                    self.cpus.remove(cc)
        self.updateCores()

    def addCores(self,cores):
        #self.cpus=self.cpus+cores
        n=len(self.cpus)
        for c in  cores:
            self.cpus.append(VirtualCpu.VirtualCpu(n, c, 'y',"running"))
            n=n+1
        self.updateCores()




    def addNodes(self,node):
        self.memoryNumaNodes= self.memoryNumaNodes+node

    def removeNodes(self,nodes):
        for n in nodes:
            self.memoryNumaNodes.remove(n)

    def setServers(self,nodeset):
        numa=Numa()
        for node in nodeset:
            s=numa.getServer(node)
            if s in self.servers:
                continue
            else:
                self.servers.append(s)

    def getServers(self):
        return self.servers 


    def setSockets(self,sockets):
        self.sockets=sockets

    def getSockets(self):
        return self.sockets


   # def setNumaNodes(self,numaNodes):
    #    self.numaNodes=numaNodes

    #def getNumaNodes(self):
       # return self.numaNodes


    def setMemoryNumaNodes(self,memoryNodes):
        self.memoryNumaNodes=memoryNodes

    def getMemoryNumaNodes(self):
        return self.memoryNumaNodes

    def getName(self):
        return self.name


    def setvCpus(self, vCpus):
        self.vCpus=vCpus

    def getvCpus(self):
        return self.vCpus

    
    def setSoloIPC(self,soloIPC):
        self.soloIPC=soloIPC

    def getSoloIPC(self):
        return self.soloIPC


    def setSoloMPI(self,soloMPI):
        self.soloMPI=soloMPI

    def getSoloMPI(self):
        return self.soloMPI



    def setIPC(self,IPC):
        self.IPC=IPC

    def getIPC(self):
        return self.IPC

    def setMPI(self,MPI):
        self.MPI=MPI

    def getMPI(self):
        return self.MPI

    def isUsed(self,core):
        return (core in self.vCpus)


         #return the object if  cores allocated for the application are under  the server
    def coresInServer(self,server):
        if server in self.servers:
            return self
        else:
         return None



        #return the object if  cores allocated for the application are under  the socket
    def coresInSocket(self,socket):
        if socket in self.sockets:
            return self
        else:
         return None 


        #return the object if cores allocated for the application are under Numa nodes
    def coresInNode(self,numaNode):
        if numaNode in self.numaNodes:
            return self
        else:
         return None 

      #return the object if memory allocated for the application are under Numa nodes
    def momeryInNode(self,memoryNode):
        if memoryNode in self.memoryNumaNodes:
            return self
        else:
         return None 

         #relative deviation MPI from solo
    def mpiDeviation(self):
        if self.soloMPI==0.0:
            self.soloMPI=1.0
        return (self.soloMPI-self.MPI)/self.soloMPI

        #relative IPC deviation from solo
    def ipcDeviation(self):
        if self.soloIPC==0.0:
            self.soloIPC=1.0
        return (self.soloIPC-self.IPC)/self.soloIPC



    def printMe(self):
        print "VirtualApplication: " + str(self.VirtualApplication)
        print("vCpus: "),
        for n in self.vCpus:
           print(" " + str(n.no))

    #Assumes a one-to-one mapping between virtual and physical cores
    def actuate(self):
        vNo=0
        for core in self.vCpus:
            Actuator.pinVcpuToCore(self.virtualapplication, vNo, core)
            vNo=vNo+1