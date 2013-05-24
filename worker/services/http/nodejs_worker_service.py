from subprocess import Popen, PIPE
from worker.services.base_worker_service import BaseWorkerService
from master.tools import get_open_port
import json
import os

class NodejsWorkerService(BaseWorkerService):
    
    def __init__(self, transport):
        self.PORT = get_open_port()
        # Prepare the class so the notify_ready method can be called
        self.set_master_transport(transport)
        self.set_ready_message(json.dumps({'type': 'service-ready', 'service': 'http', 'port': self.PORT}))
    
    def start(self):
        print "Starting HTTP Worker Service... "
        server_path = os.path.join(os.path.dirname(__file__), 'server.js')
        self.process = Popen(["node", server_path, str(self.PORT)], stdout=PIPE)
        success = False
        
        # Read pipe for ready signal
        for line in iter(self.process.stdout.readline,''):
            print "[node-server]: %s" % line.rstrip()
            if line.rstrip() == "READY": 
                success = True
                break # Break stout readline to notify server about success
        # Notify
        if success:
            self.notify_ready()
            print "SUCCESS"
        else:
            print "ERROR"
        
    def stop(self):
        self.process.kill()
        print "Stopped HTTP Worker Service"
        
        
    def install(self):
        pass
        #TODO: MAKE INSTALL CODE
        
if __name__ == "__main__":
    worker = NodejsWorkerService()
    worker.start()
    #time.sleep(5)
    #worker.stop()