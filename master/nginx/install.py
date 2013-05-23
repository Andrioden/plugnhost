# ADD PROJECT FOLDET TO PATH
import os, sys
sys.path.insert(0,os.sep.join(os.path.abspath(__file__).split(os.sep)[:-3]))

# Step 0: Do INSTALL STEPS
"""
sudo apt-get update
sudo apt-get install python-software-properties python g++ make
sudo add-apt-repository ppa:chris-lea/node.js
sudo apt-get update
sudo apt-get install nodejs

npm install express
pip install zope.interface
pip install twisted
"""

# Step 1: Create a sites-pre-enabled directory at /etc/nginx/
print "Creating special pre enabled directory...",
import os
from settings import NGINX_DIR
pre_enabled_dir = NGINX_DIR+"sites-pre-enabled"
if not os.path.exists(pre_enabled_dir):
    os.makedirs(pre_enabled_dir)
print "SUCCESS"
    
# Step 2: Copy plugnhost site definition file to pre enabled sites directory
print "Copying site definition file...",
import shutil

file = os.path.join(os.path.dirname(__file__), 'plugnhost')
shutil.copy2(file, pre_enabled_dir)
print "SUUCESS"

# Step 3: Edit the nginx.conf file to include pre-enabled sites at the top of
#         the http scope
print "Editing nginx.conf file...",
import fileinput

found = False
for line in fileinput.input(NGINX_DIR+"nginx.conf", inplace=1):
    if line.startswith('http {'):
        found = True # Next line will have a preprinted string
    else:
        if found:
            print "\t#Next line allows a upstream site to be added on top of http scope"
            print "\tinclude /etc/nginx/sites-pre-enabled/*;"
            print "\n"
        found = False
    print line,
print "SUCCESS"