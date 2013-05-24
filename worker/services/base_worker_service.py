class BaseWorkerService(object):
    
    def set_master_transport(self, master_transport):
        self.master_transport = master_transport
    def set_ready_message(self, ready_message):
        self.ready_message = ready_message
    
    def notify_ready(self):
        """ Notifies the master that the service is ready """
        self.master_transport.write(self.ready_message)