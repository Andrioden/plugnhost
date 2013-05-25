from subprocess import call
from tools import download
import os

def install_windows():
    # Step 1: Install node.js
    node_path = download("http://nodejs.org/dist/v0.10.8/","node-v0.10.8-x86.msi")
    if node_path:
        print "Installing Node.JS...",
        call('msiexec /i %s' % node_path, shell=True)
        print "DONE (unless you cancelled, you fool?)"
    else:
        print "Failed to install NodeJS"
        return
    # Step 2: Install Node Module: Express
    print "Installing Node Module: Express..."
    here_path = os.path.dirname(__file__)
    node_modules_folder = os.path.join(os.path.dirname(__file__), 'node_modules')
    if not os.path.exists(node_modules_folder):
        os.makedirs(node_modules_folder)
    call("npm install --prefix %s express" % here_path, shell=True)
    print "...Successfully installed Node Module: Express"
    # Step 3: Install zope.interface (twisted depends on it)
    zope_path = download("http://pypi.python.org/packages/2.7/z/zope.interface/","zope.interface-4.0.5.win32-py2.7.exe")
    if zope_path:
        print "Installing zope.interface...",
        call(zope_path, shell=True)
        print "DONE (unless you cancelled, you fool?)"
    else:
        print "Failed to install zope.interface"
        return
    # Step 4: Install Twisted
    twisted_path = download("https://pypi.python.org/packages/2.7/T/Twisted/","Twisted-13.0.0.win32-py2.7.msi")
    if twisted_path:
        print "Installing Twisted...",
        call('msiexec /i %s' % twisted_path, shell=True)
        print "DONE (unless you cancelled, you fool?)"
    else:
        print "Failed to install twisted"
        
if __name__ == "__main__":
    install_windows()