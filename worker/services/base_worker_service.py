from tools import get_open_port
import json

class BaseWorkerService(object):
    
    def __init__(self):
        self.PORT = get_open_port()
    
    def set_master_transport(self, master_transport):
        self.master_transport = master_transport
        
    def set_service_name(self, service_name):
        self.service_name = service_name
        
    def notify_ready(self, data=None):
        """ Notifies the master node that the service is ready """
        ready_message = {'type': 'service-ready',
                         'service': self.service_name,
                         'port': self.PORT}
        if data:
            ready_message['data'] = data
        self.master_transport.write(json.dumps(ready_message))