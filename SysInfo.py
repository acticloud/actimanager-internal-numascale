'''
Implements different methods/classes to get static as well as dynamic state of the physical machine and VMs
'''
from __future__ import print_function
import os
import subprocess
import Driver
import libvirt
import VirtualMachine
import re
import DriverVirsh
import psutil # requires installation of psutil library i.e., sudo apt-get install python-psutil
from xml.dom import minidom
from xml.etree import ElementTree
from PerfCounter import PerfCounter

class SysInfo(object):

    def __init__(self, systemState):
        print("Calling SysInfo constructor")
        self.systemState = systemState
        self.hostname = self.systemState.hostname
        print("SysInfo constructor Called")
        self.perfCounter = PerfCounter()

    def getDomainInfo(self, domain):
        dom = Driver.getDomainByID(domain)
        name = dom.name()
        id = domain
        host = self.systemState.hostname
        type = "silver"
        if name.lower().startswith("g"):
            type = "gold"
        vm = VirtualMachine.VirtualMachine(domain, name, id, host, type)
        return vm

    def getIPC(self, cores):
        return self.perfCounter.getIPC(cores)

    def getMPI(self,cores):
        return self.perfCounter.getMPI(cores)

    def getHostCPUMap():
        try:
            return Driver.getHostCPUMap()

        except libvirt.libvirtError:
            print('Failed to get host CPU Map')
            sys.exit(1)

    def getVcpusCpuMaps(domainID):
        try:
            return Driver.getVcpusCpuMaps(domainID)

        except libvirt.libvirtError:
            print('Failed to get vcpu map')
            sys.exit(1)

    def getNodeSet(self, domainID):
        try:
            return DriverVirsh.getNodeSet(domainID)

        except libvirt.libvirtError:
            print('Failed to get Node info')
            sys.exit(1)

    def getMemorySize(self, domainID):
        try:
            return DriverVirsh.getMemorySize(domainID)

        except libvirt.libvirtError:
            print('Failed to get memory size info')
            sys.exit(1)

    def getVcpusInfo(self, domainID):
        try:
            return Driver.getVcpusInfo(domainID)

        except libvirt.libvirtError:
            print('Failed to get vcpu info')
            sys.exit(1)

    def getTotalCores(self):
        """ Number of available virtual or physical CPUs on this system, i.e.
        user/real as output by time(1) when called with an optimally scaling
        userspace-only program"""

        # cpuset
        # cpuset may restrict the number of *available* processors
        try:
            m = re.search(r'(?m)^Cpus_allowed:\s*(.*)$',
                          open('/proc/self/status').read())
            if m:
                res = bin(int(m.group(1).replace(',', ''), 16)).count('1')
                if res > 0:
                    return res
        except IOError:
            pass
        # Python 2.6+
        try:
            import multiprocessing
            return multiprocessing.cpu_count()
        except (ImportError, NotImplementedError):
            pass
        # Windows
        try:
            res = int(os.environ['NUMBER_OF_PROCESSORS'])
            if res > 0:
                return res
        except (KeyError, ValueError):
            pass
        # BSD
        try:
            sysctl = subprocess.Popen(['sysctl', '-n', 'hw.ncpu'],
                                      stdout=subprocess.PIPE)
            scStdout = sysctl.communicate()[0]
            res = int(scStdout)
            if res > 0:
                return res
        except (OSError, ValueError):
            pass
        # Linux
        try:
            res = open('/proc/cpuinfo').read().count('processor\t:')
            if res > 0:
                return res
        except IOError:
            pass
        # Solaris
        try:
            pseudoDevices = os.listdir('/devices/pseudo/')
            res = 0
            for pd in pseudoDevices:
                if re.match(r'^cpuid@[0-9]+$', pd):
                    res += 1
            if res > 0:
                return res
        except OSError:
            pass
        # Other UNIXes (heuristic)
        try:
            try:
                dmesg = open('/var/run/dmesg.boot').read()
            except IOError:
                dmesgProcess = subprocess.Popen(['dmesg'], stdout=subprocess.PIPE)
                dmesg = dmesgProcess.communicate()[0]

            res = 0
            while '\ncpu' + str(res) + ':' in dmesg:
                res += 1
            if res > 0:
                return res
        except OSError:
            pass
        raise Exception('Can not determine number of CPUs on this system')

    def getPMMemoryStat(self):

        stats = psutil.virtual_memory()
        swap = psutil.swap_memory()
        return stats, swap

    def NetIOStat(self):

        stat = psutil.net_io_counters()
        return stat

    def getCPUStat(self, perCPU=False):
        stat = psutil.cpu_times(percpu=perCPU)
        percent = psutil.cpu_percent(percpu=perCPU);

        return stat, percent;

    '''
    get hardware temperature
    requires  installation of lm-sensors library (i.e., sudo apt-get install lm-sensors)
    Return hardware temperatures. 
    Each entry is a named tuple representing a certain hardware temperature sensor 
    (it may be a CPU, an hard disk or something else, depending on the OS and its configuration).
     All temperatures are expressed in celsius unless fahrenheit is set to True. 
     If sensors are not supported by the OS an empty dict is returned. Example:
    '''

    def getTemp(self):
        if not hasattr(psutil, "sensors_temperatures"):
            sys.exit("platform not supported or upgrade your psutil version")
            temps = psutil.sensors_temperatures()  # availble starting from version  5.1.0.
            return temps

    # returns the NUMA topology as a list(per NUMA Node):
    def getNUMATopology(self):
        capsXML = Driver.getNUMATopology()
        caps = minidom.parseString(capsXML)
        host = caps.getElementsByTagName('host')[0]
        cells = host.getElementsByTagName('cell')
        print (cells.length)
        numa = []
        # iterate through the xml object to get the NUMA topology
        for cell in cells:
            node_id = cell.getAttribute('id')
            print (cell.firstChild.nodeValue)
            memory = cell.getElementsByTagName('memory')[0].firstChild.nodeValue
            distances = {proc.getAttribute('id'): proc.getAttribute('value')
                         for proc in cell.getElementsByTagName('sibling')
                         }  # if proc.getAttribute('id'): proc.getAttribute('value') not in distances }
            cores = [proc.getAttribute('id')
                     for proc in cell.getElementsByTagName('cpu')
                     ]
            node = {node_id: [memory, distances, cores]}
            numa.append(node)

        return numa

    # return VM memory stat
    def getVMMemoryStat(domainName):

        conn, dom = Driver.connectToDomain(domainName)

        stats = dom.memoryStats()

        conn.close()
        return stats

    # return VM CPU stat
    '''
    The getCPUStats takes one parameter, a boolean. 
    When False is used the statistics are reported as an aggregate of all the CPUs. 
    When True is used then each CPU reports its individual statistics. 
    Either way a list is returned. The statistics are reported in nanoseconds. 
    If a host has four CPUs, there will be four entries in the cpu_stats list.
    For more: https://libvirt.org/docs/libvirt-appdev-guide-python/en-US/html/libvirt_application_development_guide_using_python-Guest_Domains-Monitoring-vCPU.html 
    '''

    def getVMCPUStat(domainName, perCPUStat=True):

        conn, dom = Driver.connectToDomain(domainName)

        stats = dom.getCPUStats(perCPUStat)

        conn.close()
        return stats

    # Returns Network stat for a domain as a list:
    #     'read bytes:    ' stats[0]
    #     'read packets:  '+ stats[1]
    #     'read errors:   '+stats[2]
    #     'read drops:    '+stats[3]
    #     'write bytes:   '+stats[4]
    #     'write packets: '+stats[5]
    #     'write errors:  '+stats[6]
    #     'write drops:   '+stats[7]
    def getNetworkIOStat(domainName):

        conn, dom = Driver.connectToDomain(domainName)

        tree = ElementTree.fromstring(dom.XMLDesc())
        iface = tree.find('devices/interface/target').get('dev')
        stats = dom.interfaceStats(iface)

        conn.close()
        return stats

        # get cpu and momory info about the domain

    def getDomainStat(self, domainName):
        conn, dom = Driver.connectToDomain(domainName)

        if dom == None:
            print('Failed to find the domain ' + domainName, file=sys.stderr)
            exit(1)

        state, maxmem, mem, cpus, cpuTime = dom.info()

        conn.close()

        return state, maxmem, mem, cpus, cpuTime