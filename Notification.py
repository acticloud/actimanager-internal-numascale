'''
This class implements communication service between different ACTiCLOUD components using RabbitMQ. 
It contains both the message producer and receiver codes.
'''
import pika #Helps to handle the underlying communication to and from RabbitMQ server(http://pika.readthedocs.io
import pickle # to serialize python object
import json
from VirtualMachine import VirtualMachine
class Notification(object):

    def __init__(self, config, mqExchangeName):
        
        self.rabbitMQ_info= config.getRabbitMQ_Info()
        self.connection=None
        self.channel=None
        self.message=None
        self.mqExchangeName=mqExchangeName

    def RabbitMQConnection(self):
        credentials = pika.PlainCredentials(self.rabbitMQ_info['rabbitUser'], self.rabbitMQ_info['rabbitPassword'])#set credentials
        self.connection = pika.BlockingConnection(pika.ConnectionParameters( self.rabbitMQ_info['rabbitHost'],self.rabbitMQ_info['rabbitPort'],'/',credentials)) # Connect to RabbitMQ server
        self.channel = self.connection.channel() # creates  a TCP channel
        
    def closeConnection(self):
        self.connection.close();
        
        #follows puplish/subscribe communication pattern. Notification can be sent to multiple subscribers
    def notify(self, message):
        self.channel.exchange_declare(exchange=self.mqExchangeName,# subscribers should use the same exchange name to get notification
                         exchange_type='fanout')
        self.channel.basic_publish(exchange=self.mqExchangeName,
                      routing_key='',
                      body=pickle.dumps(message) #Serialize the Message object  as you can't send native Python types as your payload.
                      )

    ''' ------Sample method- This is where listen, receiving events and  processing of events happen----
     ---- should be implemented accordingly-----
    Receiving messages from the queue is made by   subscribing  to a callback function to a queue. 
    Whenever we receive a message, this callback function is called by the Pika library. 
    In our case the  function returns the  message sent by the producer through the notify() method call.
    '''

    def callback(self, ch, method, properties, body):
        message=pickle.loads(body) #Deserialize the Message object
        print("  Received message %r" % message.getMessageType()+ " "+ message.getBody())
        
        ''' @param
            exchangeName: the name of the exchange where the producer sends its message
            callback: the name of the callback method that  gets notified when a message is delivered to the exchange.
                     A sample callback method is implemented above
        '''
    def receive(self,callback):
        
        # exchangeName should be the same name used by the publisher (i.e.,by  notify() method)          
        self.channel.exchange_declare(exchange=self.mqExchangeName,
                                        exchange_type='fanout')
        
        ''' create temporary queue for storing notification messages till they are pick-up by the consumer. 
          The operation is idempotent. Rabbit mq will be responsible in managing the queue( assigning names, deletion, etc)
        '''
        result = self.channel.queue_declare(exclusive=True)
        queueName = result.method.queue
        
        #make a connection between the queue and the exchange.
        self.channel.queue_bind(exchange=self.mqExchangeName,
                   queue=queueName)

        self.channel.basic_consume(callback, queue=queueName)
        self.channel.start_consuming()

    def getStatusMessage(self, systemState, pmInfo):
        virtualMachines = systemState.virtualMachines

        data = {}
        data["hostname"] = pmInfo.pmName
        data["cpuload]"] = pmInfo.cpuPercent
        data["memload"] = pmInfo.memPercent

        evict_string = ""
        perfalert_string = ""

        for vm in virtualMachines:
            if vm.isEvictionCandidate:
                evict_string += str(vm.domain)+","
            if vm.performanceAlert:
                perfalert_string += str(vm.domain)+","

        data["eviction_candidates"] = evict_string
        data["performance_alerts"] = perfalert_string

        json_data = json.dumps(data)
        print "Constructing status message: "+str(json_data)
        return json_data


        self.log(pmInfo.pmName, pmInfo.cpus, pmInfo.cpuPercent, pmInfo.memSize, pmInfo.memPercent)
