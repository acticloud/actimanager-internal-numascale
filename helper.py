'''
This helper module contains helper classes and/or methods
'''


'''a class that defines the type of message communicated among components 
(equivalent to enum as older version of python doesn't explicitly support enum). 
'''
class MType(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError
    
    #add the type of messages  in the list
MessageType = MType(['Interference', 'Overload', 'Underload', 'Mapping'])    

'''
The Message class implements the data structure that is to notify other components 
 '''
class Message:

    def __init__(self,  messageType, body):
      
        self.messageType=messageType 
        self.body=body #actual content of the message( this can be in any format e.g., json, xml, etc)
    
    def getBody(self):
        return self.body
    
    def getMessageType(self):
        return self.messageType
    
    
# if __name__ == "__main__":
#     message=Message(MessageType.Interference,'Hello')
#     print message.getMessageType()+message.getBody()