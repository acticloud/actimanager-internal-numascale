import os
import sys
import libvirt
import subprocess
import collections
import VirtualCpu
from xml.dom import minidom
import re


#if running remote, export LIBVIRT_DEFAULT_URI="qemu+tcp://ac01.ds.cs.umu.se/system" in bashrc

#This is quite messy. the python libvirt api does not support getting the vcp->core mapping information
#so we are running virsh and parsing the output. Not very nice...
def getVcpusInfo(domainID):
    try:
        cpumap = subprocess.check_output("virsh vcpuinfo " +str(domainID), shell=True)
        vcpustr = str.split(cpumap, "VCPU:")
        vcpus = []

        for vcpu in vcpustr:
            if str.__len__(vcpu) > 0:
                vcpuno = None
                cpuno = None
                state = None
                time = None
                pinned = None
                vcpudata = str.splitlines(vcpu)
                for data in vcpudata:
                    if str.startswith(data, " "):
                        vcpuno = getVcpu(data)
                    if str.startswith(data, "CPU:"):
                        cpuno = getCpu(data)
                    if str.startswith(data, "State:"):
                        state = getState(data)
                    if str.startswith(data, "CPU time:"):
                        time = getTime(data)
                    if str.startswith(data, "CPU Affinity:"):
                        pinned = str(getPinned(data))
                vcpus.append(VirtualCpu.VirtualCpu(vcpuno,cpuno,pinned,state))
                #print "Found vCPU " + vcpuno + " mapped to core " + cpuno + " pinned: " + pinned

    except libvirt.libvirtError:
        print('Failed to get vcpu info')
        sys.exit(1)

    return vcpus

def getVcpu(data):
    return data.strip()

def getDomainIP(domainID):
    print "Getting local IP for domain " + str(domainID)
    try:
      response = subprocess.check_output("virsh domifaddr " + str(domainID) , shell=True)
      #print "Virsh response: " + str(response)
      ipstr = str.split(response, "ipv4")[1]
      ipstr2 = str.split(ipstr, "/")[0].strip()
    except:
      ipstr2 = "-1"
    print "IP is: " + str(ipstr2)
    return ipstr2

def getCpu(data):
    return str.split(data, "CPU:")[1].strip()

def getState(data):
    return str.split(data, "State:")[1].strip()

def getTime(data):
    return str.split(data, "CPU time:")[1].strip()

#nodeset syntax = "0-n" example node 1-3 = "1-3"
def pinMemory(domain, nodeset):
    print "Moving memory fpr domain " + str(domain) + " to node " + str(nodeset)
    response = subprocess.check_output("virsh numatune " + str(domain) + " --nodeset " + str(nodeset), shell=True)
    print "Numatune response: " + str(response)
    return response

def getPinned(data):
    affinity = str.split(data, "CPU Affinity:")[1]
    counts = collections.Counter(affinity)

    for i in affinity:
        if i == "y":
            nocores = counts[i]
            if nocores == 1:
                return True

    return False



def getNodeSet(domainID):
    dumpxml = subprocess.check_output("virsh dumpxml " + str(domainID), shell=True)
    xml = minidom.parseString(dumpxml)
    nodeset=[proc.getAttribute("nodeset")
                for proc in xml.getElementsByTagName("memory")]
    nodes=[]
    for node in nodeset:
        if node.strip()!="":
                nodes=nodes+re.split("[ ,-]", node)

    return nodes

def getMemorySize(domainID):
    dumpxml = subprocess.check_output("virsh dumpxml " + str(domainID), shell=True)
    xml = minidom.parseString(dumpxml)
    memoryTag=xml.getElementsByTagName("currentMemory")
    memorySize = float( memoryTag[0].firstChild.nodeValue)/1024

    return memorySize


