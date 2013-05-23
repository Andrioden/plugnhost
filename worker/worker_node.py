# ADD PROJECT FOLDET TO PATH
import os, sys
sys.path.insert(0,os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))

# NORMAL IMPORTS
from twisted.internet import reactor, protocol
import json
from settings import COMMUNICATION_PORT
from http_worker_service import HttpWorkerService
from master.tools import get_open_port

class WorkerNode(protocol.Protocol):
    
    services = []
    
    def start(self):
        """ Start all services """
        http_port = get_open_port()
        http_service = HttpWorkerService(http_port)
        # Prepare the class so the notify_ready method can be called
        http_service.set_master_transport(self.transport)
        http_service.set_ready_message(json.dumps({'type': 'service-ready', 'service': 'http', 'port': http_port}))
        # Attempt to start the service
        http_service.start() 
        self.services.append(http_service)
    
    def stop(self):
        for service in self.services:
            service.stop()
    
    def connectionMade(self):
        self.start()
    
    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        data = json.loads(data)
        print "Server said:", data
        #self.transport.loseConnection()
    
    def connectionLost(self, reason):
        print "connection lost"

class WorkerNodeFactory(protocol.ClientFactory):
    protocol = WorkerNode

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed - goodbye!"
        reactor.stop()
    
    def clientConnectionLost(self, connector, reason):
        print "Connection lost - goodbye!"
        reactor.stop()

if __name__ == '__main__':
    f = WorkerNodeFactory()
    host = "localhost"
    reactor.connectTCP(host, COMMUNICATION_PORT, f)
    print "Connection to master on port %s:%S " % (host, COMMUNICATION_PORT)
    reactor.run()