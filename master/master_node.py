# ADD PROJECT FOLDET TO PATH
import os, sys
sys.path.insert(0,os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))

# NORMAL IMPORTS
from twisted.internet import reactor, protocol
import json
import settings

""" A Twisted application server, will listen on a given PORT for worker nodes 
communication

 """
class MasterNode(protocol.Protocol):
    workers = []
    service_handlers = {}
    
    def connectionMade(self):
        print "connection from - ", self.transport.getPeer()

    def dataReceived(self, data):
        """ Data received from a worker node """
        try:
            data = json.loads(data)
            print data
            if data['type'] == "service-ready":
                self.new_worker_service(self.transport.getPeer().host, data['port'], data['service'])
        except ValueError as err:
            print err
            print "Got data non-JSON: %s " % data
    
    def connectionLost(self, reason):
        print "Connection lost - ", self.transport.getPeer()
        self.lost_worker_host(self.transport.getPeer().host)
        
    def new_worker_service(self, host, port, service_name):
        if self._add_service_handler(service_name):
            worker = self._get_worker(host)
            if not worker:
                worker = Worker(host)
                self.workers.append(worker)
            worker.services.append(WorkerService(service_name, host, port))
            print "-- Worker(+) %s" % worker
            self.on_worker_change(service_name)
        else:
            print "Failed to add %s to the service pool" % service_name
        
    def lost_worker_host(self, host):
        for worker in self.workers:
            if worker.IP == host:
                print "-- Worker(-) %s" % worker
                # Remove worker
                self.workers.remove(worker)
                # Notify service handlers about worker amount change
                for service in worker.services:
                    self.on_worker_change(service.name)

                
    def on_worker_change(self, service_name):
        current_worker_services = self._get_worker_services(service_name)
        print "---- Current %s workers (%s): %s" % (service_name, len(current_worker_services), current_worker_services)
        self.service_handlers[service_name].on_worker_change(current_worker_services)
                
    def _get_worker(self, host):
        for worker in self.workers:
            if worker.IP == host:
                return worker
        return False
    
    def _get_worker_services(self, service_name):
        all_worker_services = []
        for worker in self.workers:
            this_worker_servies = worker.get_services_with_name(service_name)
            all_worker_services.extend(this_worker_servies)
        return all_worker_services
        
    def _add_service_handler(self, service_name, reload_allowed=True):
        """ Adds the service handler class for a given service name. 
        The service handler class is attempted eval'd from the settings module, 
        if not found the settings module is reloaded, and the method runs 
        itself recursively once more. The settings module is reloaded so new 
        services can be introduces live.
        
        """
        if self.service_handlers.has_key(service_name):
            return True
        else:
            try:
                path_class = settings.SERVICES[service_name]['MasterClass'].rsplit(".", 1)
                exec ("from %s import %s" % (path_class[0], path_class[1]))
                self.service_handlers[service_name] = eval(path_class[1]+"()")
                print "Added %s to the service pool" % service_name
                return True
            except Exception as err:
                print "Failed to add sevice handler: %s, err: %s" % (service_name, err)
                if reload_allowed:
                    print "Reloading settings module and trying again"
                    reload(settings) # Reload settings module in case of changes
                    return self._add_service_handler(service_name, False) # Avoid endless loop
                else:
                    return False
        
class Worker(object):
    def __init__(self, IP):
        self.IP = IP
        self.services = []
        
    def get_services_with_name(self, service_name):
        return_services = []
        for service in self.services:
            if service.name == service_name:
                return_services.append(service)
        return return_services
    
    def __repr__(self):
        return "Worker - %s - %s" % (self.IP, self.services)
    
class WorkerService(object):
    def __init__(self, name, IP, PORT):
        self.IP = IP
        self.PORT = PORT
        self.name = name
        
    def __repr__(self):
        return "%s@%s:%s" % (self.name, self.IP, self.PORT)
        
if __name__ == '__main__':
    # Start listening for worker connections
    factory = protocol.ServerFactory()
    factory.protocol = MasterNode
    reactor.listenTCP(settings.COMMUNICATION_PORT, factory)
    print "Waiting for worker connections on port %s " % settings.COMMUNICATION_PORT
    reactor.run()