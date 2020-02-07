import libvirt
import sys


#qemuUri = 'qemu+tcp://ac01.ds.cs.umu.se/system'
qemuUri = 'qemu:///system'
#qemuUri = 'test:///default'

def openReadOnly():
    try:
        print('Connection to ' + qemuUri)
        conn = libvirt.openReadOnly(qemuUri)
        print('Connected to ' + conn.getHostname())
    except libvirt.libvirtError:
        print('Failed to connect to the hypervisor')
        sys.exit(1)
    return conn

def connectToHypervisor():
    try:
        conn = libvirt.open(qemuUri)
    except libvirt.libvirtError:
        print('Failed to connect to to qemu') #, file =s ys.stderr
        sys.exit(1)

    return conn

def getDomainByName(domainName):
    
    conn = connectToHypervisor()

    try:
        dom = conn.lookupByName(domainName)
    except libvirt.libvirtError:
        print('Failed to find the domain ' + domainName) #, file =s ys.stderr
        exit(1)
    return dom


def getDomainByID(domainID):
    conn = connectToHypervisor()

    try:
        dom = conn.lookupByID(domainID)
        #print dom.name()
    except libvirt.libvirtError:
        print('Failed to find the domain ' + domainName)  # , file =s ys.stderr
        exit(1)
    return dom

def getActiveDomains():
    conn = connectToHypervisor()

    domainIDs = conn.listDomainsID()
    if domainIDs is None:
        print('Failed to get a list of domain IDs')
    conn.close()
    return domainIDs

def getHostCPUMap():
    conn = connectToHypervisor()

    map = conn.getCPUMap(0)
    if map is None:
        print('Failed to get host CPU Map')
    conn.close()
    return map

def getVcpusCpuMaps(domainID):
    try:
        domain = getDomainByID(domainID)
        print (domain.isActive())
        vcpuinfo = domain.get(1, cpumap)

    except libvirt.libvirtError:
        print('Failed to get vcpu map')
        sys.exit(1)
    return vcpuinfo

def getNUMATopology():
    try:
        conn = libvirt.openReadOnly(None)
    except libvirt.libvirtError:
        print('Failed to connect to the hypervisor')
        sys.exit(1)

    try:
        capsXML = conn.getCapabilities()
    except libvirt.libvirtError:
        print('Failed to request capabilities')
        sys.exit(1)

    return capsXML

def pinVcpuToCore(domainID, vcpuno, cpumap):
    try:

        domain = getDomainByID(domainID)
        #print cpumap
        domain.pinVcpu(vcpuno, cpumap)
    except libvirt.libvirtError:
        print('Failed to pin vcpu')
        sys.exit(1)

def setVcpus(domainID, vcpus):
    try:
        domain = getDomainByID(domainID)
        print (domain.isActive())
        domain.setVcpus(vcpus)
    except libvirt.libvirtError:
        print('Failed to set number of vcpu')
        sys.exit(1)


'''A Domain instance has the following info:
for domain in domains:
        print(' ID '+str(domain.ID()))
        print(' Name '+domain.name())
        print('UUID  '+domain.UUIDString())
        print('OSType  '+domain.OSType())
        print('hasCurrentSnapshot  '+str(domain.hasCurrentSnapshot()))
        print(' hasManagedSaveImage '+str(domain.hasManagedSaveImage()))
      #  print(' hostname '+str(domain.hostname()))
        print(' isActive() '+str(domain.isActive()))
        print(' isPersistent '+str(domain.isPersistent()))
        print(' maxMemory '+str(domain.maxMemory()))
        print(' maxVcpus '+str(domain.maxVcpus()))
        state, maxmem, mem, cpus, cput = domain.info()
        print('The state is ' + str(state))
        print('The max memory is ' + str(maxmem))
        print('The memory is ' + str(mem))
        print('The number of cpus is ' + str(cpus))
        print('The cpu time is ' + str(cput))
        state, reason = domain.state()
        if state == libvirt.VIR_DOMAIN_NOSTATE:
            print('The state is VIR_DOMAIN_NOSTATE')
        elif state == libvirt.VIR_DOMAIN_RUNNING:
            print('The state is VIR_DOMAIN_RUNNING')
        elif state == libvirt.VIR_DOMAIN_BLOCKED:
            print('The state is VIR_DOMAIN_BLOCKED')
        elif state == libvirt.VIR_DOMAIN_PAUSED:
            print('The state is VIR_DOMAIN_PAUSED')
        elif state == libvirt.VIR_DOMAIN_SHUTDOWN:
            print('The state is VIR_DOMAIN_SHUTDOWN')
        elif state == libvirt.VIR_DOMAIN_SHUTOFF:
            print('The state is VIR_DOMAIN_SHUTOFF')
        elif state == libvirt.VIR_DOMAIN_CRASHED:
            print('The state is VIR_DOMAIN_CRASHED')
        elif state == libvirt.VIR_DOMAIN_PMSUSPENDED:
            print('The state is VIR_DOMAIN_PMSUSPENDED')
        else:
            print(' The state is unknown.')
        print('The reason code is ' + str(reason))
            

'''

def getAllDomains():

    conn = connectToHypervisor()

    try:
        domains = conn.listAllDomains(0)
    except libvirt.libvirtError:
        print('Failed to get All get All Domains ') #, file =s ys.stderr
        exit(1)

    return domains




