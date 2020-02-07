from VirtualApplication import VirtualApplication
from SysInfo import SysInfo
from SystemState import SystemState
from Matcher import Matcher
import time

class ApplicationManager:

	#list of virtual application currently running
	def __init__(self, systemState, time):
		self.virtualApplications = []
		self.ts = time
		self.systemState = systemState
		self.sysinfo = SysInfo(systemState)

	def isOverbooked(self, core):
		counter = 0
		for vApp in self.virtualApplications:
			if vApp.isUsed(core):
				counter = counter+1
				if counter > 1:
					return True
		return False

	def getAppInfo(self, vm):
		app = VirtualApplication(vm)
		return app

	def initVirtualApplications(self, vmlist):
		for vm in vmlist:
			app = self.getAppInfo(vm)
			app.setIPC(self.sysinfo.getIPC(app.cores))
			app.setMPI(self.sysinfo.getMPI(app.cores))
			self.setConfigValues(app)
			self.virtualApplications.append(app)
		return self.virtualApplications

	def save(self, apps):
		fileNameUtil = "expt/"+str(self.ts) + "cpu_Util" + ".csv"
		stat, percent = self.sysinfo.getCPUStat(perCPU=True)
		#CPU stat save
		util = str(percent)[1:-1]
		f = open(fileNameUtil,"a+")
		f.write(util)
		f.write("\n")
		f.close()

		#memory stat save
		filememoryNameUtil = "expt/" + str(self.ts) + "memory_Util" + ".csv"
		stat, swap = self.sysinfo.getPMMemoryStat()
		f = open(filememoryNameUtil, "a+")
		for s in stat:
			f.write(str(s) + ",")
		f.write(str(" ") + ",")
		for s in swap:
			f.write(str(s) + ",")

		f.write("\n")
		f.close()

		for app in self.virtualApplications:
			fileName = "expt/"+str(self.ts)+"_"+app.getName()+".csv"
			f = open(fileName,"a+")
			timestamp = time.time()

			f.write(str(timestamp) + ",")
			f.write(str(app.soloIPC)+",")
			f.write(str(app.IPC) + ",")
			f.write(str(app.soloMPI) + ",")
			f.write(str(app.MPI) + ",")
			f.write(app.className+",")
			f.write(str(app.memoryNumaNodes) + ",")
			f.write(str(app.memorySize) + ",")
			f.write(str(app.cores))

			f.write("\n")
			f.close()

	def setConfigValues(self, app):
		if "fft" in app.name:
			app.setSoloIPC(0.2021655)
			app.setSoloMPI(18.04446)
			app.setClassName("Devil")
		elif "neo4j" in app.name:
			app.setSoloIPC(0.7460726)
			app.setSoloMPI(2.199126)
			app.setClassName("Sheep")
		elif "sockshop" in app.name:
			app.setSoloIPC(0.4478513)
			app.setSoloMPI(11.62649)
			app.setClassName("Sheep")

		elif "derby" in app.name:
			app.setSoloIPC(0.4743592)
			app.setSoloMPI(3.857252)
			app.setClassName("Sheep")

		elif "sunflow" in app.name:
			app.setSoloIPC(0.7995293)
			app.setSoloMPI(0.9885339)
			app.setClassName("Rabbit")

		elif "sor" in app.name:
			app.setSoloIPC(0.4441287)
			app.setSoloMPI(0.1577804)
			app.setClassName("Devil")
		elif "mpegaudio" in app.name:
			app.setSoloIPC(1.368156)
			app.setSoloMPI(0.05943198)
			app.setClassName("Rabbit")

		elif "stream" in app.name:
			app.setSoloIPC(0.4743592)
			app.setSoloMPI(3.85725)
			app.setClassName("Sheep")

	def isIdle(self,core):
		for vApp in self.virtualApplications:
			if vApp.isUsed(core):
				return False
		return True


	def actuate(self ):
		for vApp in self.virtualApplications:
			vApp.actuate()

	# comparator for sorting applications by number of numa nodes
	def nodeNoCompare(self, x, y):
		return int(y.memorySize)- int(x.memorySize)
		# if len(x.getMemoryNumaNodes()) > (y.getMemoryNumaNodes()):
		# 	return 1
		# elif (x.getMemoryNumaNodes()) == (y.getMemoryNumaNodes()):
		# 	return 0
		# else:
		# 	return -1

	# sort by Number of nodes
	def sortByNoNodes(self, appList):
		return sorted(appList, cmp = self.nodeNoCompare)
		#sorted(appList, key=lambda application: application[0])
		#return appList.sort(self.nodeNoCompare)

	#comparator for sorting applications by MPI deviation
	def mpiCompare(self, x, y):

	   return int(((y.soloMPI -y.MPI) / y.soloMPI) * 1000) - int(((x.soloMPI - x.MPI) / x.soloMPI) * 1000)

	#comparator for sorting applications by IPC deviation
	def ipcCompare(self,x, y):
	   return int( ((x.soloIPC-x.IPC)/x.soloIPC)*1000) - int(((y.soloIPC-y.IPC)/x.soloIPC)*1000)

	#comparator for sorting applications by the number of  cores
	def noCoresCompare(self,x, y):
	   return len(x.getvCpus()) - len(y.getvCPUs())


	#sort by IPC deviation
	def sortByIPCDeviation(self, appList):
		return sorted(appList,cmp = self.ipcCompare)

	 #sort by MPI deviation
	def sortByMPIDeviation(self, appList):
		return sorted(appList,cmp = self.mpiCompare)

	#sort by the number of cores allocated to applications
	def sortByNoCores(self, appList):
		return sorted(appList, cmp = self.noCoresCompare)

	def getCollocatedApplications(self, domain, domainNumber):
		# returns list of applications in domain(memoryNode, numa,socket or server) given the domain number
		collocatedApps = []

		if domain == "memoryNode":
			for app in self.virtualApplications:
				if app.memoryInNode(domainNumber) != None:
					collocatedApps.append(app)

		elif domain == "numa":
			for app in self.virtualApplications:
				if app.coresInNode(domainNumber) != None:
					collocatedApps.append(app)

		elif domain == "socket":
			for app in self.virtualApplications:
				if app.coresInSocket(domainNumber) != None:
					collocatedApps.append(app)
		elif domain == "server":
			for app in self.virtualApplications:
				if app.memoryInNode(domainNumber) != None:
					collocatedApps.append(app)

		return collocatedApps

	#return applications whose IPC deviation is above a threshold
	def getIPCAffectedApps(self, threshold):
		affectedApps = []
		for app in self.virtualApplications:
			if app.ipcDeviation() > threshold:
				affectedApps.append(app)

		return affectedApps

	#return applications whose MPI deviation is above a threshold
	def getMPIAffectedApps(self, threshold):
		affectedApps = []
		for app in self.virtualApplications:
			if app.mpiDeviation() > threshold:
				affectedApps.append(app)
		return affectedApps

	#get applications that run only on a given  PM
	def getAppsInServer(self,server):
		appsInServer = []
		for app in self.virtualApplications:
			if  len(app.getServers()) == 1:
				appsInServer.append(app)

	#get applications that share
	def resolveViolation(self, metrics, threshold):
		#get  applications whose performance is affected
		if metrics == "MPI":
			affectedApps=self.getMPIAffectedApps(threshold)
		else:
			affectedApps = self.getIPCAffectedApps(threshold)

		if len(affectedApps) == 0: # all applications are behaving well
			return

	   #get list of servers where apps are affected
		servers = []
		for app in affectedApps:
			set(servers).union(set(app.getServers()))

		for s in servers:
			# get apps that runs only on that server
			appsInServer = self.getAppsInServer(s)
			# get applications sorted by relative IPC deviation (the most affected apps will be at the top)
			if metrics == "MPI":
				sortedApps = self.sortByMPIDeviation(appsInServer)

			else:
				sortedApps = self.sortByIPCDeviation(appsInServer)
			# match the most affected apps with the least affected
			self.match(sortedApps)

	def match(apps):
		match = Matcher()
		match.allocate(apps)
		match.allocateWithMemoryMigration(apps, 80)

	# perform server loadbalancing-- this is most likely a rare event and requires momory movement.
	def loadBalance(self):
		#self.initVirtualApplication(mon, virtualMachines)
		#print self.virtualApplications
		sortedApp = self.sortByNoNodes(self.virtualApplications)
		#print sortedApp

		match = Matcher()
		match.next_fit(sortedApp)
		return sortedApp

	def decide(self, metrics, threshold):
		#self.initVirtualApplication(mon,virtualMachines)
		self.resolveViolation(metrics, threshold)
		#self.actuate()

		return self.virtualApplications

	def printApps(self, sortedApp):
		for app in sortedApp:
			print app.name + str(app.memoryNumaNodes)
