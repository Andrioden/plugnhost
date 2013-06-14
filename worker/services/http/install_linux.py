from subprocess import call
import os

def install_linux():
    call("sudo apt-get update", shell=True)
    call("sudo apt-get install python-software-properties python g++ make", shell=True)
    call("sudo add-apt-repository ppa:chris-lea/node.js", shell=True)
    call("sudo apt-get update", shell=True)
    call("sudo apt-get install nodejs", shell=True)
    call("sudo apt-get install pip", shell=True)
    call("pip install zope.interface", shell=True)
    call("apt-get install python-twisted", shell=True)
    
    here_path = os.path.dirname(__file__)
    call("npm install --prefix %s express" % here_path, shell=True)
    
    """
    sudo apt-get update
    sudo apt-get install python-software-properties python g++ make
    sudo add-apt-repository ppa:chris-lea/node.js
    sudo apt-get update
    sudo apt-get install nodejs
    
    npm install express
    pip install zope.interface
    apt-get install python-twisted
    """
    
if __name__ == "__main__":
    install_linux()