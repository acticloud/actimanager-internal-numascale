from MappingAlgBase import MappingAlgBase
from SysDescr import SysDescr
import random
from MapTriple import MapTriple
import VirtualMachine

class RandomMapping(MappingAlgBase):

    vcpu_map = []

    def get_vpcu_map(self, mon, vmlist, metrics, threshold,time):
        #calculate a random mapping
        self.get_mapping(vmlist)
        return self.vcpu_map

    def get_mapping(self, virtualMachines):
        print("--- Performing Random mapping ---")
        for vm in virtualMachines:
            # vm.printMe()
            self.mapVM(vm, False)


    def mapVM(self, vm, spread):
         nocores = len(vm.vCpus)
         print "VM has "+str(nocores)+" cores"
         remaining = nocores

         sysDescr = SysDescr()

         for vcpu in range(0,nocores):
            core_alloc = random.randint(0,sysDescr.totalCores-1)
            mapTriple = MapTriple(vm.domain, vcpu, core_alloc)
            print "Mapping vcpu "+str(vcpu)+" to core "+str(core_alloc)
            self.vcpu_map.append(mapTriple)
