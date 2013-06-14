from subprocess import Popen, PIPE
from worker.services.base_worker_service import BaseWorkerService
import os

class NodejsWorkerService(BaseWorkerService):
    
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
            print "...HTTP Worker Service ONLINE"
        else:
            print "...Failed to start HTTP Worker Service"
        
    def stop(self):
        self.process.kill()
        print "Stopped HTTP Worker Service"
        
    def install(self):
        if os.name == "nt": # Running on Windows
            from install_windows import install_windows
            install_windows()
        elif os.name == "posix":
            from install_linux import install_linux
            install_linux()
        else:
            print "OS Not supported"
        
if __name__ == "__main__":
    worker = NodejsWorkerService()
    worker.start()