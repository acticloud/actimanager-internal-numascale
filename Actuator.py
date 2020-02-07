import libvirt
import Driver

from ast import literal_eval

class Actuator:

    def pinVcpuToCore(self, domainID, vcpuno, core):
        try:
            print "Pinning vcpu: " + str(vcpuno) + " for domain " + str(domainID) + " to core " + str(core)
            cpumap = "("
            if core == 0:
                cpumap += "1,0)"
                return Driver.pinVcpuToCore(domainID, vcpuno, literal_eval(cpumap))
            else:
                for i in range(core):
                    cpumap += "0, "
            cpumap += "1)"
            cpulist = literal_eval(cpumap)
            return Driver.pinVcpuToCore(domainID, vcpuno, cpulist)

        except libvirt.libvirtError:
            print('Failed to pin vcpu ')
            sys.exit(1)

    def setVcpus(domainID, vcpus):
        try:
            return Driver.setVcpus(domainID, vcpus)

        except libvirt.libvirtError:
            print('Failed to set number of vcpus')
        sys.exit(1)

    def pinMemory(self, domainID, nodeset):
        try:
            print "Actuator.pinMemory"
            return Driver.pinMemory(domainID, nodeset)

        except libvirt.libvirtError:
            print('Failed to pin memory')
        sys.exit(1)



