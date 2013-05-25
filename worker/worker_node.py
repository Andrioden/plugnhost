# ADD PROJECT FOLDET TO PATH
import os, sys
sys.path.insert(0,os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))

# NORMAL IMPORTS
from twisted.internet import reactor, protocol
import json
import settings

class WorkerNode(protocol.Protocol):
    
    services = []
    
    def start(self):
        """ Start all services """
        for service_name in settings.SERVICES:
            path_class = settings.SERVICES[service_name]['WorkerClass'].rsplit(".", 1)
            exec ("from %s import %s" % (path_class[0], path_class[1]))
            service = eval(path_class[1]+"()")
            service.set_master_transport(self.transport)
            service.set_service_name(service_name)
            service.start()
            self.services.append(service)
    
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
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        host = "andresh.nerdvana.tihlde.org"
        #host = "localhost"
    f = WorkerNodeFactory()
    reactor.connectTCP(host, settings.COMMUNICATION_PORT, f)
    print "Connection to master on port %s:%s " % (host, settings.COMMUNICATION_PORT)
    reactor.run()