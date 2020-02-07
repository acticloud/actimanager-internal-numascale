from Monitoring import Monitoring
from VMMonData import VMMonData
from PMMonData import PMMonData
from SysInfo import SysInfo
import time
import libvirt


class Utilization:

    def __init__(self, systemState):
        self.prevCpuTime = 0
        self.prevTimestamp = 0
        self.monitoring = Monitoring(systemState)
        self.cpus = ""
        self.prevCpuTime = ""
        self.prevTimestamp = ""
        self.sysinfo = SysInfo(systemState)

    def getVMUtilization(self, domainName):
        state, maxmem, mem, cpus, cputime = self.monitoring.getDomainStat(domainName)

        if not (state in [libvirt.VIR_DOMAIN_SHUTOFF, libvirt.VIR_DOMAIN_CRASHED]):
            self.cpus = cpus
            curCPUTime = cputime - self.prevCpuTime
            self.prevCpuTime=cputime
            now = time.time()
            pcentbase = (((curCPUTime) * 100.0) /
                         ((now - self.prevTimestamp) * 1000.0 * 1000.0 * 1000.0))
            pcentGuestCpu = pcentbase / self.cpus
            self.prevTimestamp = now
            pcentCurrMem = mem * 100.0 / maxmem

        pcentGuestCpu = max(0.0, min(100.0, pcentGuestCpu))
        pcentCurrMem = max(0.0, min(pcentCurrMem, 100.0))

        vmUtil = VMMonData(domainName, cpus, pcentGuestCpu, maxmem, pcentCurrMem)
        return vmUtil

    def getPMUtilization(self):
        import platform
        name = platform.node()
        cpus = self.sysinfo.getTotalCores()
        cpuStat, pcentHostCpu = self.sysinfo.getCPUStat()
        memStat, swap = self.sysinfo.getPMMemoryStat()
        pcentHostMem = memStat[2]
        memSize = memStat[0]
        mpUtil=PMMonData(name, cpus, pcentHostCpu, pcentHostMem, memSize)

        return mpUtil