import DriverLibvirt
import DriverVirsh

system='KVM'

def openReadOnly():
    if system == 'KVM':
        return DriverLibvirt.openReadOnly()
    else:
        raise Exception('Support for % not implemented', system)
        sys.exit(1)

def connectToDomain(domainName):
    if system == 'KVM':
        conn =DriverLibvirt.connectToHypervisor()

        dom = DriverLibvirt.getDomainByName(domainName)
        return conn, dom
    else:
        raise Exception('Support for %s not implemented', system)
        sys.exit(1)

def getDomainByName(domainName):
    if system == 'KVM':
        return DriverLibvirt.getDomainByName(domainName)
    else:
        raise Exception('Support for %s not implemented', system)
        sys.exit(1)


def getDomainByID(domainID):
    if system == 'KVM':
        return DriverLibvirt.getDomainByID(domainID)
    else:
        raise Exception('Support for %s not implemented', system)
        sys.exit(1)


def getNUMATopology():
    if system == 'KVM':
        return DriverLibvirt.getNUMATopology()
    else:
        raise Exception('Support for %s not implemented', system)
        sys.exit(1)


def getActiveDomains():
    if system == 'KVM':
        return DriverLibvirt.getActiveDomains()
    else:
        raise Exception('Support for %s not implemented', system)
        sys.exit(1)


def getHostCPUMap():
    if system == 'KVM':
        return DriverLibvirt.getHostCPUMap()
    else:
        raise Exception('Support for %s not implemented', system)
        sys.exit(1)

def getDomainIP(domainID):
    if system == 'KVM':
        return DriverVirsh.getDomainIP(domainID)
    else:
        raise Exception('Support for %s not implemented', system)
        sys.exit(1)

def pinMemory(domain, nodeset):
    if system == 'KVM':
        return DriverVirsh.pinMemory(domain, nodeset)
    else:
        raise Exception('Support for %s not implemented', system)
        sys.exit(1)

def getVcpusInfo(domainID):
    if system == 'KVM':
        return DriverVirsh.getVcpusInfo(domainID)

    else:
        raise Exception('Support for %s not implemented', system)
        sys.exit(1)


def pinVcpuToCore(domainID, vpcu, cpumap):
    if system == 'KVM':
        return DriverLibvirt.pinVcpuToCore(domainID, vpcu, cpumap)
    else:
        raise Exception('Support for %s not implemented', system)
        sys.exit(1)


def setVcpus(domainID, vcpus):
    if system == 'KVM':
        return DriverLibvirt.setVcpus(domainID, vcpus)
    else:
        raise Exception('Support for %s not implemented', system)
        sys.exit(1)









