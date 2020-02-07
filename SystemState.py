#holds the runtime state of the host
import time
from PMMonData import PMMonData

class SystemState(object):

    def __init__(self, uri, hostname):
        self.uri = uri
        self.hostname = hostname
        self.virtualMachines = []
        self.pmInfo = PMMonData
        self.overloadThreshold = 50
        self.underLoadThreshold = 10
        self.imbalanceRatio = 5
        self.stateTimestamp = time.time()
        self.loadTimestamp = time.time()


    def updateVirtualMachines(self, virtualMachines):
        self.virtualMachines = virtualMachines
        self.stateTimestamp = time.time()

    def getVirtualMachines(self):
        return self.virtualMachines

    def updateLoad(self, pmInfo):
        self.pmInfo = pmInfo
        self.loadTimestamp = time.time()

    def getLoad(self):
        return self.pmInfo

    # uses simple threshold based on CPU Utilization
    def isOverload(self):

        if float(self.pmInfo.cpuPercent) >= float(self.overloadThreshold):
            return True
        else:
            return False

    #check overloaded VMs
    def isVMOverload(self,vmInfo):

        if float(self.pmInfo.cpuPercent) >= float(self.overloadThreshold):
            return True
        else:
            return False

    # uses simple threshold based on CPU Utilization
    def isUnderload(self):

        if self.pmInfo.cpuPercent <= self.underloadThreshold:
            return True
        else:
            return False

    #check underloaded VMs
    def isVMUnderload(self, vmInfo):

        if self.vmInfo.cpuPercent() <= self.underloadThreshold:
            return True
        else:
            return False

    # check whether there is a memory-cpu imbalance
    def isImbalance(self):
        cpuPercent = self.pmInfo.cpuPercent
        memPercent = self.pmInfo.memPercent
        imbRatio = max(cpuPercent / memPercent,
                       memPercent / cpuPercent)  # signals the applications are either cpu or memory bound (implies one of the resources is wasted)
        if imbRatio > self.imbalanceRatio:
            return True
        else:
            return False
