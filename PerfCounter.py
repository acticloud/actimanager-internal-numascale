from subprocess import check_output
import subprocess
import re
import time
import multiprocessing

class PerfCounter:
    def __init__(self):
        #commands
        self.numaConnectCMD=["./nc_perf_loop_all.sh", "./nc_perf_short_loop_all.sh","./nc_perf_read_all.sh"]
        self.numaNodeCMD="numastat"

        self.coreCMD="perf kvm --guest stat -a  -A  -x, -e LLC-load-misses -e cpu-cycles -e instructions -e cache-misses sleep "

        self.socketCMD="perf kvm --guest stat -a  --per-socket -x, -e LLC-load-misses -e cpu-cycles -e instructions -e cache-misses sleep 0"

        #Per physical machine performance counters
        # 0--5 where the value at index 0 is the numa connect cache misses for PM1
        self.numaConnectMisses=[]
        # 0--5 where the value at index 0 is the numa connect cache misses for PM1
        self.numaConnectHit=[]

        #per numa node performance counter
        # 0--35 where the value at index 0 is the cache misses for the first NUMA node
        self.numaNodeMisses=[]

        #Per socket performance counters
        # 0--17 where the value at index 0 is the LLC  misses for the first socket
        self.socketMisses=[]
        # 0--17 where the value at index 0 is the CPU-Cycle for the first socket
        self.socketCPUCycle=[]
        # 0--17 where the value at index 0 is the number of instructions for the first socket
        self.socketInstructions=[]
        # 0--17 where the value at index 0 is the cache misses  for the first socket
        self.socketCacheMisses=[]

        #Per physical core performance counters
        # 0--144 where the value at index 0 is the LLC  misses for the first core
        self.coreMisses=[]
        # 0--144 where the value at index 0 is the CPU-Cycle for the first core
        self.coreCPUCycle=[]
        # 0--144 where the value at index 0 is the number of instructions for the first core
        self.coreInstructions=[]
        # 0--144 where the value at index 0 is the number of caches misses for the first core
        self.coreCacheMisses=[]



    def clearList(self):
        self.numaConnectMisses[:]=[]
        self.numaConnectHit[:]=[]
        self.numaNodeMisses[:]=[]
        self.socketMisses[:]=[]
        self.socketCPUCycle[:]=[]
        self.socketInstructions[:]=[]
        self.socketCacheMisses[:]=[]
        self.coreMisses[:]=[]
        self.coreCPUCycle[:]=[]
        self.coreInstructions[:]=[]
        self.coreCacheMisses[:]=[]

    #collect performance counter every interval-seconds
    def startMonitoring (self,interval):
        while True:
            self.probe(interval)
            time.sleep(interval)

    #write to a file
    def write(self,fileName, data):
        f=open(fileName,"a+")
        for d in data:
            f.write(d+",")
        f.write("\n")
        f.close()




    #probe performance counter commands
    def probe(self,interval):
        self.clearList()
       # outputNNC_perf_loop_all=self.runCommand(self.numaConnectCMD[0])
        #outputNNC_perf_short_loop_all=self.runCommand(self.numaConnectCMD[1])
        #outputNNC_perf_read_all=self.runCommand(self.numaConnectCMD[2])

        outputNumaNode=self.runCommand(self.numaNodeCMD)
        outputSocket=self.runCommand(self.socketCMD)
        outputPhysicalCore=self.runCommand(self.coreCMD+ str(interval))

        #parse counter values

        #NUMA CONNECT
#         self.parseNCCMisses(outputNNC_perf_loop_all, "Total")
#         #log the NCC performance counter
#         self.write("result/numaConnectMisses.csv", self.numaConnectMisses)
#         self.write("result/numaConnectHits.csv", self.numaConnectHit)
#
# #######
#         self.saveNCCMisses ("result/nc_perf_short_loop_all_Misses.csv", "result/nc_perf_short_loop_all_Hits.csv",outputNNC_perf_short_loop_all, "Total")
#
#         self.saveNCCMisses ("result/nc_perf_read_all_misses.csv", "result/nc_perf_read_all_Hits.csv",outputNNC_perf_read_all, "Total")

        #NUMA NODE
        self.parseNumaNodeMisses(outputNumaNode,"numa_miss")


        #save other details of Numa nodes
        self.saveNumaNodeInfo("result/numa_hit.csv", outputNumaNode,"numa_hit")
        self.saveNumaNodeInfo("result/numa_foreign.csv", outputNumaNode,"numa_foreign")
        self.saveNumaNodeInfo("result/interleave_hit.csv", outputNumaNode,"interleav_hit")
        self.saveNumaNodeInfo("result/local_node.csv", outputNumaNode,"local_node")
        self.saveNumaNodeInfo("result/other_node.csv", outputNumaNode,"other_node")

        ##total cores in the Physical machine
        self.totalCores=multiprocessing.cpu_count()


        #log NUMA NODE misses
        self.write("result/numaNodeMisses.csv", self.numaNodeMisses)
        #socket

        #print(outputNNC_perf_loop_all)
        #print(self.numaConnectMisses)
        #print(self.coreMisses)
        #print(self.coreInstructions)
        #print(self.coreCPUCycle)
        #print(self.coreCacheMisses)
        #print(outputPhysicalCore)
        self.parseSocketCounters(outputSocket)
        #log socket performance counter
        self.write("result/socketMisses.csv", self.socketMisses)
        self.write("result/socketCPUCycle.csv", self.socketCPUCycle)
        self.write("result/socketInstructions.csv", self.socketInstructions)
        self.write("result/socketCacheMisses.csv", self.socketCacheMisses)
        #physical cores
        self.parsePCCounters(outputPhysicalCore)
        #log physical core performance counter
        self.write("result/coreMisses.csv", self.coreMisses)
        self.write("result/coreCPUCycle.csv", self.coreCPUCycle)
        self.write("result/coreInstructions.csv", self.coreInstructions)
        self.write("result/coreCacheMisses.csv", self.coreCacheMisses)

        # print(self.coreMisses)
        # print(self.coreInstructions)
        # print(self.coreCPUCycle)
        # print(self.coreCacheMisses)

#parses and save the numa node info from the performance counter output

    def saveNumaNodeInfo(self,fileName, output,pattern):
        lines =output.splitlines()
        numaNodeInfo=[]
        for i in range(len(lines)):

            str=self.parseOutput(pattern, lines[i])
            if str !=None:
                token =lines[i].split()
                for j in range(len(token)-1):
                    numaNodeInfo.append(token[j+1])
            #save to file
        self.write(fileName, numaNodeInfo)


    #parses and save the numa connect performance counter output
    def saveNCCMisses (self,fileNameMisses, fileNameHits,output, pattern):

        lines =output.splitlines()
        j=0
        numaMisses=[]
        numaHit=[]
        for i in range(len(lines)):
            str=self.parseOutput(pattern, lines[i])
            #print (str)
            #print("HHHHHHHHHHHHHHHHHHHHHH"+pattern+lines[i])
            #print (str)
            if str !=None:
                token=lines[i].split()
                #print("HHHHHHHHHHHHHHHHHHHHHH"+token[6]+lines[i])
                numaMisses.append(token[6])
                numaHit.append(token[11])
                j=j+1
        self.write(fileNameMisses,numaMisses)
        self.write(fileNameHits,numaHit)

    def runCommand(self,cmd):

        output = check_output (cmd, shell = True, stderr=subprocess.STDOUT)

        return output


    def parseOutput(self,pattern, output):

        matchObj = re.search(pattern, output)

        if matchObj:
            return matchObj.group()
        else:
            return None;


    #parses the numa node misses from the performance counter output

    def parseNumaNodeMisses(self,output,pattern):
        lines =output.splitlines()
        #print (lines)
        for i in range(len(lines)):
            str=self.parseOutput(pattern, lines[i])
            if str !=None:
                token =lines[i].split()
                #print(token)
                for j in range(len(token)-1):
                    self.numaNodeMisses.append(token[j+1])


    #parse performance counter for each physical cores
    def parsePCCounters(self,output):
        index=0;
        lines =output.splitlines()
        for i in range(len(lines)):
            token=lines[i].split(",")
            if i/self.totalCores==0:
                self.coreMisses.append(token[1])

            elif i/self.totalCores==1:
                self.coreCPUCycle.append(token[1])
            elif i/self.totalCores==2:
                self.coreInstructions.append(token[1])
            elif i/self.totalCores==3:
                self.coreCacheMisses.append(token[1])
                index=index + 1


#parse performance counter for each socket
    def parseSocketCounters(self,output):
        index=0;
        lines =output.splitlines()
        #print ("LLLLLLLLLLLLLLLLLLLLLLLLLLLLL#####################")
        #print(output)
        for i in range(len(lines)):
            token=lines[i].split(",")
            if i%4==0:
                self.socketMisses.append(token[2])

            elif i%4 == 1:
                self.socketCPUCycle.append(token[2])
            elif i%4 == 2:
                self.socketInstructions.append(token[2])
            elif i%4 == 3:
                self.socketCacheMisses.append(token[2])
                index=index+1


    #parses the numa connect performance counter output
    def parseNCCMisses (self,output, pattern):

        lines =output.splitlines()
        j=0
        for i in range(len(lines)):
            str=self.parseOutput(pattern, lines[i])
            if str !=None:
                token=lines[i].split()

                self.numaConnectMisses.append(token[6])
                self.numaConnectHit.append(token[11])
                j=j+1

    #returns the  IPC for a VM given the list of cores that the VM is running
    def getIPC(self, interval, cores):
        self.probe(1)

        CPUCycle=0.0
        instruction=0.0
        for i in cores:
            CPUCycle+=float(self.coreCPUCycle[int(i)])
            instruction+=float(self.coreInstructions[int(i)])

        if CPUCycle==0.0:
            CPUCycle =1.0

        return instruction/CPUCycle

    #returns the  MPI for a VM given the list of cores that the VM is running
    def getMPI(self, cores):

        misses=0.0
        instruction=0.0
        for i in cores:
            misses+=float(self.coreMisses[int(i)])
            instruction+=float(self.coreInstructions[int(i)])

        if instruction== 0.0:
            instruction=1.0

        return misses/instruction

if __name__ == "__main__":
    perfCounter=PerfCounter()
    perfCounter.startMonitoring(5)
