import random
from time import sleep

class Interference:

    def __init__(self, systemState):
        ''' Constructor for this class. '''
        print "Calling Interference detection constructor"
        self.systemState = systemState

    def detect_interference(self):
        for i in range(1, 15):
            sleep(1)
            if bool(random.getrandbits(1)):
                print "Interference detected!!"

    def start(self):
        print("Interference detection started")
        self.detect_interference()
        print("Interference detection finished")



