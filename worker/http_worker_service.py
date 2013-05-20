from subprocess import Popen
import time

class HttpWorkerService(object):
    
    PORT = "81"
    process = None
    
    def start(self):
        print "Starting HTTP Worker Service"
        self.process = Popen(["node", "server.js", self.PORT])
        
    def stop(self):
        self.process.kill()
        print "Stopped HTTP Worker Service"
        
if __name__ == "__main__":
    worker = HttpWorkerService()
    worker.start()
    #time.sleep(5)
    #worker.stop()