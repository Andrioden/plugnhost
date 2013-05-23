from subprocess import Popen, PIPE
import time
from worker_service import WorkerService

class HttpWorkerService(WorkerService):
    
    PORT = None
    process = None
    
    def __init__(self, port):
        self.PORT = port
    
    def start(self):
        print "Starting HTTP Worker Service... "
        self.process = Popen(["node", "server.js", str(self.PORT)], stdout=PIPE)
        success = False
        # First wait for ready signal
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
        
if __name__ == "__main__":
    worker = HttpWorkerService()
    worker.start()
    #time.sleep(5)
    #worker.stop()