# ADD PROJECT FOLDET TO PATH
import os, sys
sys.path.insert(0,os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))

# NORMAL IMPORTS
from twisted.internet import reactor, protocol
import json
from settings import COMMUNICATION_PORT
from tools import nginx_reqwrite_site_config,

""" A Twisted application server, will listen on a given PORT for worker nodes 
communication

 """
class MasterNode(protocol.Protocol):
    workers = []
    
    def connectionMade(self):
        print "connection from - ", self.transport.getPeer()

    def dataReceived(self, data):
        try:
            data = json.loads(data)
            print data
            if data['type'] == "service-ready":
                if data['service'] == "http":
                    self.new_worker(Worker(self.transport.getPeer().host, data['port']))
            #self.transport.write(json.dumps())
        except ValueError as err:
            print err
            print "Got data non-JSON: %s " % data
    
    def connectionLost(self, reason):
        print "Connection lost - ", self.transport.getPeer()
        self.lost_worker_host(self.transport.getPeer().host)
        #TODO: Remove worker with ip
        
    def new_worker(self, worker):
        self.workers.append(worker)
        print "-- Worker(+) %s" % worker
        self.on_worker_change()
        
    def lost_worker_host(self, host):
        for worker in self.workers:
            if worker.IP == host:
                print "-- Worker(-) %s" % worker
                self.workers.remove(worker)
                self.on_worker_change()
                
    def on_worker_change(self):
        print "---- Current workers (%s): %s" % (len(self.workers), self.workers)
        nginx_reqwrite_site_config(self.workers)
        
class Worker(object):
    IP = None
    PORT = None
    
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT
    
    def __repr__(self):
        return "Worker - %s:%s" % (self.IP, self.PORT)
        
if __name__ == '__main__':
    factory = protocol.ServerFactory()
    factory.protocol = MasterNode
    reactor.listenTCP(COMMUNICATION_PORT, factory)
    print "Listening to port %s " % COMMUNICATION_PORT
    reactor.run()