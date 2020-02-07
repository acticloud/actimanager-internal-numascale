from VirtualApplication import VirtualApplication
from matching import Player
from matching import StableMarriage
from Numa import Numa
import DriverVirsh
class Matcher:

	def __init__(self):
		self.numa = Numa()


	#applications sorted by memory size in descending order
	def next_fit(self,sortedApps):
		numaSize=self.numa.getNumaSize() #in MB
		coresPerNuma=self.numa.getCoresPerNode()
		numNumaNodes=  self.numa.getNodes()

		coresPerServer= self.numa.getCoresPerServer()

		servers = self.numa.numServers
		nodesetSize= []
		allCores=[]
		for i in range(0,numNumaNodes):
			nodesetSize.insert(i, numaSize)

		for i in range(0,servers):
			allCores= allCores + self.numa.getCoresInServer(i)

		allCores.sort()

		numaIndex=numNumaNodes-1

		#first allocate memory for those applications with full memory nodes
		for app in sortedApps:
			name= app.getName()
			size= app.memorySize
			noCores=len(app.cpus)
			nodes= int(size/numaSize)
			nodeSet=[]
			cores= []
			if nodes >0:
				for i in range (0,nodes):
					if numaIndex < -1:
						break
					nodeSet.append(numaIndex)
					nodesetSize[numaIndex] = 0.0
					numaIndex = numaIndex - 1




				# coresPerNuma = coresPerNuma[coresPerNuma:]
				end=len(allCores)
				start=end-noCores
				cores = allCores[start: end]
				allCores = allCores[0:start]
				#print "AAAAAA" + str(allCores)+ "length:" + str(len(allCores)) + "\n\n" +str(cores)+ "length:" + str(len(cores))



				app.setMemoryNumaNodes(nodeSet)
				app.cpus = cores
			#print app.name + " cores:" + str(len(app.cpus)) + " \n"
		# first allocate memory for those applications with fractional memory nodes


		for app in sortedApps:
			name = app.getName()
			size = app.memorySize
			noCores = len(app.cpus)
			nodes = int(size / numaSize)
			numaIndex = numNumaNodes - 1
			nodeSet = []
			cores = []

			if nodes == 0:

				for i in range (0, numNumaNodes):


					if size <= nodesetSize[numaIndex]:
						server = self.numa.getServer(numaIndex)
						coresInServer = self.numa.getCoresInServer(server)

						cores =list(set(allCores)& set(coresInServer))

						#print str(allCores) + "index:" + str(numaIndex) + "server" + str(server) + "cores:" + str(cores) +"cores inS:"+ str(coresInServer)
						if len(cores)>=noCores:
							#print " cores before:" + str(cores)
							end = len(cores)
							start = end - noCores
							cores = cores[start: end]
							#cores= cores[0:noCores]
							#print " cores after:"+ str(cores)+ " "+str(noCores)
							allCores= list(set(allCores)-set(cores))
							nodeSet.append(numaIndex)
							app.setMemoryNumaNodes(nodeSet)
							app.cpus = cores
							nodesetSize[numaIndex] = nodesetSize[numaIndex] - size
							print app.name +" cores:"+ str(cores) + " \n"
							#print str(nodeSet)+ "imdex:"+str(numaIndex)

							break

					numaIndex = numaIndex - 1



















	#collocates most affected apps with least affected
	def simpleAllocator(self, sortedApps):
		cores=[]
		for app in sortedApps:
			cores=cores+app.getvCpus()
		cores.sort()
		i=0
		j=0
		while i < len(sortedApps)/2:
			app=sortedApps(i)
			app.setvCpus(cores[j:app.getvCpus()])
			j=j+app.getvCpus()
			app=sortedApps(len(sortedApps)-i)
			app.setvCpus(cores[j:app.getvCpus()])
			j=j+app.getvCpus()

			i=i+1
		if len(sortedApps)%2==1:
			app=sortedApps(len(sortedApps)/2)
			app.setvCpus(cores[j:app.getvCpus()])

	def getAppByName(self,name, sortedApps):
		for app in sortedApps:
			if app.getName() == name:
				return app
		return None
	

	#based on stable matching problem concept
	def stableMatch(self,sortedApps):

		candidates= self.getPreference(sortedApps[0:len(sortedApps)/2], sortedApps)
		start=len(sortedApps)/2
		if len(sortedApps)%2==1:
			start=start+1
		match = self.getPreference(sortedApps[start:len(sortedApps)], sortedApps)
		sm = StableMarriage(candidates, match)

		match = sm.solve()
		return match

	#allocate cores based on the matching
	def allocate(self, sortedApps):
		match=self.stableMatch(sortedApps)
		assigned = []
		cores = []
		for app in sortedApps:
			cores = cores + app.getvCpus()
		cores.sort()

		for appName in match:
			app = self.getAppByName(appName,sortedApps)
			unassignedCores=self.getUnassignedCores(app.getMemoryNumaNodes(), assigned, cores)
			unassignedCores.sort()
			if len(app.vCpus) == len(unassignedCores):
				app.vCpus=unassignedCores
				assigned.append(unassignedCores)
			elif len(app.vCpus) <len(unassignedCores):
				app.vCpus= unassignedCores[0:len(app.vCpus)]
				assigned.append(unassignedCores[0:len(app.vCpus)])

			else:
				c = unassignedCores
				assigned.append(c)
				unassigned = set(assigned).symmetric_difference(cores)
				c=c+ unassigned[0:len(app.vCpus) -len(c)]
				app.vCpus = c
				assigned.append(c)



			neighborName = match[app]
			neighbor = self.getAppByName(neighborName, sortedApps)
			unassignedCores = self.getUnassignedCores(neighbor.getMemoryNumaNodes(), assigned, cores)
			unassignedCores.sort()
			if len(neighbor.vCpus) == len(unassignedCores):
				neighbor.vCpus=unassignedCores
				assigned.append(unassignedCores)
			elif len(neighbor.vCpus) <len(unassignedCores):
				neighbor.vCpus= unassignedCores[0:len(neighbor.vCpus)]
				assigned.append(unassignedCores[0:len(neighbor.vCpus)])

			else:
				c = unassignedCores
				assigned.append(c)
				unassigned = set(assigned).symmetric_difference(cores)
				c=c+ unassigned[0:len(neighbor.vCpus) -len(c)]
				neighbor.vCpus = c
				assigned.append(c)

	def allocateWithMemoryMigration(self, apps, threshold):

		#if applications are spreadout do memory-core remap.
		potentialAppToRemap = []

		spreadNodes = []
		for app in apps:
			memNodes = app.getMemoryNumaNodes()
			cores = app.getvCpus()
			ratio=0.0
			for  node in  memNodes:
				coresInNode =self.numa.getCoresInNUMANode(node)
				cNode=list(set(coresInNode) & set(cores)) #get cores that the application uses in that node
				r= float(len(cNode))/float(len(cores))
				if r ==0.0:# potential memory-cores remapping
					spreadNodes.append(node)
				ratio=ratio+r
			if ratio < threshold:
				potentialAppToRemap.append(app)

		if potentialAppToRemap:

			for pMigrate in potentialAppToRemap:
				memNodes = pMigrate.getMemoryNumaNodes()
				cores = pMigrate.getvCpus()
				migrateNodes = list(set(memNodes) & set(spreadNodes))
				coresOutOfNode = list (set (cores)- (self.getCoresInNode(cores,memNodes)))
				nodesToMigrateTo =self.getPotentialNodesToMigrateTo(coresOutOfNode)

				# migrateNodes <nodesToMigrateTo => cores are spread out, thus, do core remapping
				if len(migrateNodes)< len(nodesToMigrateTo):
					self.doCoreRemap(app,migrateNodes,coresOutOfNode,apps)

				else: #do mem migratrion
					self.doMemMigration(app,migrateNodes,nodesToMigrateTo,apps)

		else: #do normal rematch
			self.allocate(apps)



		#for x in range(len(0,apps)/2,2): #best-worst match
			#apps[x+1], apps[len(apps)-x-1] = apps[len(apps)-x-1], apps[x+1]

	def doMemMigration(self, app, migrateNodes, nodesToMigrateTo,apps):

		unAssigned = migrateNodes
		app.removeNodes(migrateNodes)
		noNodes = len(migrateNodes)
		newNodes=nodesToMigrateTo[:noNodes]
		app.addNodes(newNodes)
		app.migrate=1 #set the migrate flag.
		#move these applications whose memory is used to unassigned location
		for moveApp in apps:
			shiftedNodes=moveApp.getMemoryNumaNodes() & newNodes
			if shiftedNodes:
				moveApp.removeNodes(shiftedNodes)
				moveApp.addNodes(unAssigned[:len(shiftedNodes)])
				unAssigned = list(set(unAssigned) - set(unAssigned[:len(shiftedNodes)]))
				moveApp.migrate = 1  # set the migrate flag.






	def getCoresInNode(self,cores, nodes):

		coresInNodes=[]
		for n in nodes:
			coresInNodes=coresInNodes+ cores & self.numa.getCoresInNUMANode(n)

		return coresInNodes

	def doCoreRemap(self,app,nodesTo, cores, apps ):

		unAssigned=cores
		app.removeCores(cores)
		noCores=len(cores)
		for n in  nodesTo:
			coresInN= self.numa.getCoresInNUMANode(n)
			if noCores> len(coresInN):
				app.addcores(coresInN[:len(coresInN)])
				noCores=noCores-len(coresInN)
			else:
				app.addcores(coresInN[:noCores])
				noCores = 0

			for shiftApp in apps:
				shiftedCore=shiftApp.getvCpus()
				moved= coresInN & shiftedCore
				if moved !=None:
					shiftApp.removeCores(moved)
					shiftApp.addCores(unAssigned[:len(moved)])
					unAssigned=list(set(unAssigned) -set(unAssigned[:len(moved)]))





	def getPotentialNodesToMigrateTo(self, cores):
		potentialNodes =[]
		for core in cores:
			node= self.numa.getNodeForCore(core)
			potentialNodes.append(node)
		return list(set(potentialNodes))




	def getUnassignedCores(self, nodes, assigned, cores):
		unassigned = set(assigned).symmetric_difference(cores)

		coresAtNode=[]
		coresPerNode = self.numa.getCoresPerNode()
		for node in nodes:
			startCoreAtNode = self.numa.getStartOfCoreNodeN(node)
			for i in range(startCoreAtNode, startCoreAtNode+coresPerNode):
				coresAtNode.append(i)

		return list(set(coresAtNode) & set(unassigned)) #set(unassigned).symmetric_difference(coresAtNode)








		# very ugly code to build preference list
		def getPreference(self, apps, sortedApps):

			preferenceList = []

			for app in apps:
				pref = []


				for sApp in sortedApps:

					if app.getName() != sApp.getName() \
							and app.getClassName() == "Sheep" and sApp.getClassName() == "Devil":
						pref.append(sApp.getName())

					if app.getName() != sApp.getName() \
							and app.getClassName() == "Rabit" and sApp.getClassName() == "Sheeo":
						pref.append(sApp.getName())

					if app.getName() != sApp.getName() \
							and app.getClassName() == "Devil" and sApp.getClassName() == "Devil":
						pref.append(sApp.getName())

				for sApp in sortedApps:

					if app.getName() != sApp.getName() \
							and app.getClassName() == "Sheep" and sApp.getClassName() == "Rabit":
						pref.append(sApp.getName())

					if app.getName() != sApp.getName() \
							and app.getClassName() == "Rabit" and sApp.getClassName() == "Rabit":
						pref.append(sApp.getName())

					if app.getName() != sApp.getName() \
							and app.getClassName() == "Devil" and sApp.getClassName() == "Sheep":
						pref.append(sApp.getName())

				for sApp in sortedApps:

					if app.getName() != sApp.getName() \
							and app.getClassName() == "Sheep" and sApp.getClassName() == "Sheep":
						pref.append(sApp.getName())

					if app.getName() != sApp.getName() \
							and app.getClassName() == "Rabit" and sApp.getClassName() == "Devil":
						pref.append(sApp.getName())

					if app.getName() != sApp.getName() \
							and app.getClassName() == "Devil" and sApp.getClassName() == "Rabit":
						pref.append(sApp.getName())

				preferenceList.append(Player(name=app.getName(), pref_names=pref))

			return preferenceList






##copied

	# very ugly code to build preference list
	def getPreference1(self, apps, sortedApps):

		preferenceList = []

		for app in apps:
			pref = []
			for sApp in sortedApps:

				if app.getName() != sApp.getName() and self.common_member( \
						app.getMemoryNumaNodes(), sApp.getMemoryNumaNodes()) \
						and app.getClassName() == "Sheep" and sApp.getClassName() == "Devil":
					pref.append(sApp.getName())

				if app.getName() != sApp.getName() and self.common_member( \
						app.getMemoryNumaNodes(), sApp.getMemoryNumaNodes()) \
						and app.getClassName() == "Rabit" and sApp.getClassName() == "Sheep":
					pref.append(sApp.getName())

				if app.getName() != sApp.getName() and self.common_member( \
						app.getMemoryNumaNodes(), sApp.getMemoryNumaNodes()) \
						and app.getClassName() == "Devil" and sApp.getClassName() == "Devil":
					pref.append(sApp.getName())

			for sApp in sortedApps:

				if app.getName() != sApp.getName() and self.common_member( \
						app.getMemoryNumaNodes(), sApp.getMemoryNumaNodes()) \
						and app.getClassName() == "Sheep" and sApp.getClassName() == "Rabit":
					pref.append(sApp.getName())

				if app.getName() != sApp.getName() and self.common_member( \
						app.getMemoryNumaNodes(), sApp.getMemoryNumaNodes()) \
						and app.getClassName() == "Rabit" and sApp.getClassName() == "Rabit":
					pref.append(sApp.getName())

				if app.getName() != sApp.getName() and self.common_member( \
						app.getMemoryNumaNodes(), sApp.getMemoryNumaNodes()) \
						and app.getClassName() == "Devil" and sApp.getClassName() == "Sheep":
					pref.append(sApp.getName())

			for sApp in sortedApps:

				if app.getName() != sApp.getName() and self.common_member( \
						app.getMemoryNumaNodes(), sApp.getMemoryNumaNodes()) \
						and app.getClassName() == "Sheep" and sApp.getClassName() == "Sheep":
					pref.append(sApp.getName())

				if app.getName() != sApp.getName() and self.common_member( \
						app.getMemoryNumaNodes(), sApp.getMemoryNumaNodes()) \
						and app.getClassName() == "Rabit" and sApp.getClassName() == "Devil":
					pref.append(sApp.getName())

				if app.getName() != sApp.getName() and self.common_member( \
						app.getMemoryNumaNodes(), sApp.getMemoryNumaNodes()) \
						and app.getClassName() == "Devil" and sApp.getClassName() == "Rabit":
					pref.append(sApp.getName())

			for sApp in sortedApps:

				if app.getName() != sApp.getName() \
						and app.getClassName() == "Sheep" and sApp.getClassName() == "Devil":
					pref.append(sApp.getName())

				if app.getName() != sApp.getName() \
						and app.getClassName() == "Rabit" and sApp.getClassName() == "Sheeo":
					pref.append(sApp.getName())

				if app.getName() != sApp.getName() \
						and app.getClassName() == "Devil" and sApp.getClassName() == "Devil":
					pref.append(sApp.getName())

			for sApp in sortedApps:

				if app.getName() != sApp.getName() \
						and app.getClassName() == "Sheep" and sApp.getClassName() == "Rabit":
					pref.append(sApp.getName())

				if app.getName() != sApp.getName() \
						and app.getClassName() == "Rabit" and sApp.getClassName() == "Rabit":
					pref.append(sApp.getName())

				if app.getName() != sApp.getName() \
						and app.getClassName() == "Devil" and sApp.getClassName() == "Sheep":
					pref.append(sApp.getName())

			for sApp in sortedApps:

				if app.getName() != sApp.getName() \
						and app.getClassName() == "Sheep" and sApp.getClassName() == "Sheep":
					pref.append(sApp.getName())

				if app.getName() != sApp.getName() \
						and app.getClassName() == "Rabit" and sApp.getClassName() == "Devil":
					pref.append(sApp.getName())

				if app.getName() != sApp.getName() \
						and app.getClassName() == "Devil" and sApp.getClassName() == "Rabit":
					pref.append(sApp.getName())

			preferenceList.append(Player(name=app.getName(), pref_names=pref))

		return preferenceList




	#check if two lists a and b have common elements
	def common_member(self,a, b):
		a_set = set(a)
		b_set = set(b)
		if len(a_set.intersection(b_set)) > 0:
			return (True)
		return (False)

		# suitors = [
#     Player(name="A", pref_names=["D", "E", "F"]),
#     Player(name="B", pref_names=["D", "F", "E"]),
#     Player(name="C", pref_names=["F", "D", "E"]),
#  ]
# reviewers = [
#     Player(name="D", pref_names=["B", "C", "A"]),
#     Player(name="E", pref_names=["A", "C", "B"]),
#      Player(name="F", pref_names=["C", "B", "A"]),
#  ]
# sm = StableMarriage(suitors, reviewers)
# st=sm.solve()
# print(st) # {A: E, B: D, C: F}

