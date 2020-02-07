#from actimanagerPerfagent.PerformanceAlert.py import PerformanceAlert
from flask_restful import Resource, reqparse
import requests
import Driver
import VirtualMachine

class PerfAgentPoller:

    #Tries to poll the perfagent on the vm and returns the status or -1 if no response or an error occurs
    def pollVm(self, vm):
        status = -1
        ip = Driver.getDomainIP(vm.domain)

        if ip != "-1":
            try:
                response = requests.get("http://" + str(ip) + ":5000/performancealert/1")
                print "Response from perfalert: " + str(response)
                if response.status_code == 200:
                    json_response = response.json()
                    print json_response
                    status = str.split(str(json_response), ':')[1]
                else:
                    status = -1
            except:
                status = -1

        print "Perfalert returns status: " + str(status) + " [0 = no issues, 1 = performance issues -1 = perfagent not responding]"
        return status
