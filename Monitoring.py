'''
Implements different methods to update system state
'''
from __future__ import print_function
from time import sleep

import Driver
import psutil # requires installation of psutil library i.e., sudo apt-get install python-psutil
from Notification import Notification
from SysInfo import SysInfo
from PerfCounter import PerfCounter
from PerfAgentPoller import PerfAgentPoller
from SysInfo import  SysInfo

# returns the total number of cores in the Machine
class Monitoring:
    currentState = []

    def __init__(self, systemState):
        ''' Constructor for this class. '''
        print("Calling Monitoring constructor")

        self.perfCounter = PerfCounter()
        self.systemState = systemState
        self.sysInfo = SysInfo(systemState)
        print("Monitoring constructor Called")

    # probe hardware performance (this method should be called every period before calling getIPC and  getMisses methods) to get latest values
    def probeWPerformance(self, interval):
        self.perfCounter.probe(interval)

    # returns the  IPC for a VM given the list of cores that the VM is running
    def getIPC(self, cores):
        return self.perfCounter.getIPC(cores)

    # returns the  MPI for a VM given the list of cores that the VM is running
    def getMPI(self, cores):
        return self.perfCounter.getMPI(cores)

    def updateState(self):
        domains = Driver.getActiveDomains()
        poller = PerfAgentPoller()
        virtualMachines = []

        for domain in domains:
            dom = Driver.getDomainByID(domain)
            if dom.name() != "loadgen_sigmetrics":
                vm = self.sysInfo.getDomainInfo(domain)
                vm.setVcpus(self.sysInfo.getVcpusInfo(domain))
                vm.setNodeset(self.sysInfo.getNodeSet(domain))
                vm.setMemorySize(self.sysInfo.getMemorySize(domain))
                virtualMachines.append(vm)
                print("Found vm: " + str(vm.domain))

        # check to see if we have any new arrivals
        for vm in virtualMachines:
            match = False
            for oldVm in self.currentState:
                if (vm.domain == oldVm.domain) and (vm.id == oldVm.id):
                    print("Monitoring->getCurrentState(): This is an old VM")
                    match == True

            if match == False:
                print("Monitoring->getCurrentState(): This is a new VM")
                # vm is new, poll for existence of perf agent
                status = poller.pollVm(vm)
                if status == -1:
                    print("vm " + str(vm.domain) + " does not have a PerfAgent installed!")
                    vm.setHasPerfAgent(False)
                else:
                    print("vm " + str(vm.domain) + " has a PerfAgent installed!")
                    vm.setHasPerfAgent(True)

        #check status of perfalert
        for vm in virtualMachines:
            if vm.hasPerfAgent:
                if poller.pollVm(vm) == 1:
                    print("vm " + str(vm.domain) + " is reporting performance issues!")

        self.currentState = virtualMachines
        #self.systemState.virtualMachines = virtualMachines
        return virtualMachines

    def monitor_system(self):
        self.systemState.virtualMachines = self.updateState()


    def start(self, interval):
        print("Monitoring started")
        while True:
            self.monitor_system()
            sleep(interval)

