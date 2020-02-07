import threading
from Monitoring import Monitoring
from Interference import Interference
from Mapping import Mapping
from PMLoadDetection import PMLoadDetection
from config import Config
from Notification import Notification
from SystemState import SystemState

print "**** Actimanager Internal Numascale starting ****"
systemState = SystemState("qemu:///system", "ac02")

class MonitoringThread (threading.Thread):
    def run(self):
        #config = Config('./credentials.properties')
        #exchangeName = "am_internal_monitoring"
        #notification = Notification(config, exchangeName)
        monitoringInstance = Monitoring(systemState)
        interval = 30
        monitoringInstance.probeWPerformance(interval)
        monitoringInstance.start(interval)

#this is not implemented
#class InterferenceThread (threading.Thread):
#    def run(self):
#        interferenceInstance = Interference(systemState)
#        interferenceInstance.start()

class MappingThread(threading.Thread):
    def run(self):
        #mon = Monitoring()
        #wait till system state is initialized
        while systemState.virtualMachines is None:
            pass
        import time
        time = time.time()
        #mon.probeWPerformance(interval)
        mappingInstance = Mapping(systemState)
        mappingInstance.start_mem_pin(time);
        algorithm = "alg" # vanila or alg
        interval = 300 ##runs every five minutes
        mappingInstance.start(algorithm, time, interval)

class LoadDetectionThread (threading.Thread):
    def run(self):
        #wait till system state is initialized
        while systemState.virtualMachines is None:
            pass
        config = Config('./credentials.properties')
        exchangeName = "am_internal_status"
        notification = Notification(config, exchangeName)
        interval = 10 #this is the time interval in second where the system load is check (i.e., control Interval)
        loadDetectionInstance = PMLoadDetection(interval, notification, systemState)
        loadDetectionInstance.start(interval)

#start the monitoring thread
monitoringThread = MonitoringThread()
monitoringThread.start()

#start the load detection thread
loadDetectionThread = LoadDetectionThread()
loadDetectionThread.start()

#start the mapping thread
mappingThread = MappingThread()
mappingThread.start()

print "**** Actimanager internal started! ****"