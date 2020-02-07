#import VirtualCpu

class Core(object):

    def __init__(self, ID):
        self.ID = ID

    def mapvCpu(self, vCpu):
        self.vCpus.append(vCpu)

    def removevCpu(self, vCpu):
        self.vCpus.remove(vCpu)

    def setBusy(busy):
        self.busy = busy


