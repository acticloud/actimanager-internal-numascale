class VirtualCpu(object):

    def __init__(self, no, affinity, pinned, state):
        self.no = no
        self.affinity = affinity
        self.pinned = pinned
        self.state = state
        self.coreNo = -1

    def setCore(self, coreNo):
        self.coreNo = coreNo


