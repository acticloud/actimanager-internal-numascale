from Monitoring import Monitoring
from RandomMapping import RandomMapping
from  MappingAlgorithm import MappingAlgorithm
from time import sleep
from SystemState import SystemState
from Actuator import Actuator

class Mapping:

    def __init__(self, systemState):
        ''' Constructor for this class. '''
        print "Calling Mapping constructor"
        self.systemState = systemState


    def calculate_mapping(self, time):
        virtualMachines = self.systemState.getVirtualMachines()
        #randomMapping = RandomMapping()
        map = MappingAlgorithm()
        vcpu_map, mem_map = map.get_vpcu_map(virtualMachines, "IPC", 0.01, self.systemState,time) #MPI/ IPC

        return vcpu_map, mem_map

    def migrate_mem(self, apps):
        actuator = Actuator()
        if apps:
            for app in apps:
                domain = app.domainID
                nodes = app.memoryNumaNodes
                if len(nodes) > 1:
                    nodeset = ",".join(nodes)
                else:
                    nodeset = str(nodes)

                actuator.pinMemory(domain, nodeset)

    def start_mem_pin(self, time):
        virtualMachines = self.systemState.getVirtualMachines()
        # randomMapping = RandomMapping()
        # vcpu_map = randomMapping.get_vpcu_map(virtualMachines)

        map = MappingAlgorithm()
        vcpu_map, mem_map = map.get_mem_map(self.systemState, virtualMachines, time)
        self.perform_mem_pin(mem_map)
        actuator = Actuator()
        for map_triple in vcpu_map:
            print "mappped: "+ str(map_triple) +"\n"
            actuator.pinVcpuToCore(map_triple.domain, map_triple.vcpu, map_triple.core)

            data = str(map_triple.domain)+ " "+ str(map_triple.vcpu)+ " " +str(map_triple.core)
            self.saveConfig("cpuMap" , data)

    def saveConfig(self,fileName, data):
        f = open(fileName, "a+")
        f.write(data)
        f.write("\n")
        f.close()


    def startMatchingAlgorithm(self,time):
        actuator = Actuator()
        vcpu_map,mem_map = self.calculate_mapping(time)
        self.migrate_mem(mem_map)
        for map_triple in vcpu_map:
             actuator.pinVcpuToCore(map_triple.domain, map_triple.vcpu, map_triple.core)
        #mem_map = self.calculate_mem_map()
        #for whatever in mem_map
            # nodeset = "0-1" (eaxmple)
            # dom = Driver.getDomainByID(map_triple.domain)
            # actuator.pinMemory(dom.name(), nodeset)

    def perform_mem_pin(self,mem_map):
        actuator = Actuator()
        #print "here+++++" +str(mem_map)
        for domain, nodeset in mem_map.items():
            actuator.pinMemory(domain, nodeset)
            self.saveConfig("memMap",str(domain)+" "+str(nodeset))

    def startVanila(self,time):



        virtualMachines = self.systemState.virtualMachines
        map = MappingAlgorithm()

        map.vanila( virtualMachines,time)

    def start(self,algorithm,time,interval):
        print("Mapping thread started")

        while True:

            if algorithm == "vanila":
                print("Vanila  Algorithm Started")
                self.startVanila(time)
            else:
                print("Matching  Algorithm Started")
                self.startMatchingAlgorithm(time)


            sleep(interval)
        print("Mapping thread finished")

