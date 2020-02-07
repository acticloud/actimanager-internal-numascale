import VirtualCpu

class VirtualMachine(object):

    def __init__(self, domain, name, id, host, type):
        self.domain = domain
        self.name = name
        self.id = id
        self.host = host
        self.type = type
        self.hasPerfAgent = False
        self.placed = False
        self.performanceAlert = False
        self.hasPerfAgent = False
        self.isEvictionCandidate = False


    def setVcpus(self, vCpus):
        self.vCpus = vCpus

    def setNodeset(self, nodeset):
        self.nodeset = nodeset

    def setPerformanceAlert(self, status):
        if status == 1:
            print ("Setting PerformanceAlert for vm: "+str(domain)+" to ON")
            self.performanceAlert = True
        else:
            print ("Setting PerformanceAlert for vm: " + str(domain) + " to OFF")
            self.performanceAlert = False

    def setHasPerfAgent(self, hasPerfAgent):
        self.hasPerfAgent = hasPerfAgent

    def setIsEvictionCandidate(self, isEvictionCandidate):
        self.isEvictionCandidate = isEvictionCandidate

    def setMemorySize(self, memorySize):
        self.memorySize = memorySize

    def printMe(self):
        print "Name: " + self.name + " id " + str(self.id) + " host: " + self.host + " type: " + self.type + " domain: " + self.domain
        for vcpu in self.vCpus:
            print "VCPU: " + vcpu.no + " " + vcpu.state + " on core: " + vcpu.affinity + " pinned: " + vcpu.pinned