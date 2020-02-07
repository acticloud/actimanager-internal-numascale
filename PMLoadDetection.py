
from Utilization import Utilization
from Notification import Notification
from helper import *
import time
from time import sleep

class PMLoadDetection:

    def __init__(self, intervalInSec, notification, systemState):
        self.reportingInterval = 1
        self.util = Utilization(systemState)
        self.interval = intervalInSec
        self.notification = notification
        self.loggingTime = time.time()
        self.systemState = systemState

    def log(self, name,cpus, cpuPercent, memSize, memPercent):
        fileneme = "./utilization"+str(self.loggingTime)+".csv"
        filename = "test"  #TODO: fixme
        f = open(filename,"a+")
        f.write(name + ", " + str(cpus) + ", " + str(cpuPercent) + ", " + str(memSize) + ", " +str(memPercent))
        f.close()

    def detectLoadStatus(self):
        intervalCountoverload = 0
        intervalCountunderload = 0
        while True:
            pmInfo = self.util.getPMUtilization()
            self.log(pmInfo.pmName, pmInfo.cpus, pmInfo.cpuPercent, pmInfo.memSize, pmInfo.memPercent)
            self.systemState.updateLoad(pmInfo)

            time.sleep(self.interval)
            if self.systemState.isOverload() and ++intervalCountoverload >= self.reportingInterval: #send notification about the overload
                #virtualMachines = systemState.monitoring.getCurrentState()
                self.detectVMLoadStatus()
                statusMessage = self.notification.getStatusMessage()
                message = Message(MessageType.Overload, statusMessage)
                self.notification.RabbitMQConnection()
                self.notification.notify(message)

            elif self.systemState.isUnderload() and ++intervalCountunderload >= self.reportingInterval:
                message = Message(MessageType.Underload, pmInfo)
                self.notification.RabbitMQConnection()
                self.notification.notify(message)

            else:
                intervalCountoverload = 0
                intervalCountunderload = 0

    def detectVMLoadStatus(self):
        for vm in self.systemState.virtualMachines:
            vmInfo =self.util.getVMUtilization(vm.domain)
            if self.systemStat.isVMOverload():
                vm.setIsEvictionCandidate(True)
            else:
                vm.setIsEvictionCandidate(False)

    def start(self,interval):
        print("underload/overload detection started")

        self.detectLoadStatus()






