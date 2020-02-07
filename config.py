'''
Read different configuration values from different files to help initialize different objects.

'''
import ConfigParser
from optparse import OptionParser
class Config:
    '''Read static configuration values to initialize different objacts

   
    '''


    def __init__(self, propertyFile):
        
        self.configFile=propertyFile
       
    def getRabbitMQ_Info(self):
        # Define the names of the options
        rabbitMQ_info = {}
        option_names =  [
             'rabbitHost',
             'rabbitPort',
             'queue',
             'rabbitUser',
             'rabbitPassword',
             ]

        # Initialize the parser with some defaults
        parser = ConfigParser.SafeConfigParser(
             defaults={'rabbitHost':'localhost',
                       'rabbitPort':5672,
                       'acticloud':'acticloud',
                       'rabbitPassword':'acticloud',
                       })

        if self.configFile:
            config = ConfigParser.RawConfigParser()
            config.read(self.configFile) # Load the configuration file
            
            try:
                rabbitMQ_info["rabbitHost"] = config.get('rabbit', 'server')
            except KeyError:
                print(' missing `server` keyword')
            try:
                rabbitMQ_info["rabbitPort"] = int(config.get('rabbit', 'port'))
            except KeyError:
                print(' missing `port` keyword')   
            try:
                rabbitMQ_info["rabbitUser"]=config.get('rabbit', 'username')
            except KeyError:
                print(' missing `port` keyword')    
            try:
                rabbitMQ_info["rabbitPassword"]=config.get('rabbit', 'password')
            except KeyError:
                print(' missing `port` keyword') 
        
        return rabbitMQ_info;