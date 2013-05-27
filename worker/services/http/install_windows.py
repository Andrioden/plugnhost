from subprocess import call
from tools import download
import os, platform

# Declare dependencies that has to be downloaded
dependencies = {
    'download': {
        'Node.JS': {
            '32bit': ["http://nodejs.org/dist/v0.10.8/","node-v0.10.8-x86.msi"],
            '64bit': ["http://nodejs.org/dist/v0.10.8/x64/","node-v0.10.8-x64.msi"],
            'call': "msiexec /i %s",
        },
        'Zope.Interface': {
            '32bit': ["http://pypi.python.org/packages/2.7/z/zope.interface/","zope.interface-4.0.5.win32-py2.7.exe"],
            '64bit': ["https://pypi.python.org/packages/2.7/z/zope.interface/","zope.interface-4.0.5.win-amd64-py2.7.exe"],
            'call': "%s"
        },
        'Twisted': {
            '32bit': ["https://pypi.python.org/packages/2.7/T/Twisted/","Twisted-13.0.0.win32-py2.7.msi"],
            '64bit': ["https://pypi.python.org/packages/2.7/T/Twisted/","Twisted-13.0.0.win32-py2.7.msi"],
            'call': 'msiexec /i %s'
        }
    },
    'node_modules': ['express']
}

def install_windows():
    arch_bits = platform.architecture()[0]
    # Step 1: Install Downloadable Dependencies
    for prog_name in dependencies['download']:
        prog = dependencies['download'][prog_name]
        prog_path = download(prog[arch_bits][0], prog[arch_bits][1])
        if prog_path:
            print "Installing %s..." % prog_name, 
            call(prog['call'] % prog_path, shell=True)
            print "DONE (unless you cancelled, you fool?)"
        else:
            print "FAILED"
            
    # Step 2: Install node modules
    here_path = os.path.dirname(__file__)
    node_modules_folder = os.path.join(os.path.dirname(__file__), 'node_modules')
    if not os.path.exists(node_modules_folder):
        os.makedirs(node_modules_folder)
    for module_name in dependencies['node_modules']:
        print "Installing Node Module: %s..." % module_name
        call("npm install --prefix %s %s" % (here_path, module_name), shell=True)
        print "...Successfully installed Node Module: %s" % module_name
        
if __name__ == "__main__":
    install_windows()