# Step 0: Do INSTALL STEPS
"""
sudo apt-get update
sudo apt-get install python-software-properties python g++ make
sudo add-apt-repository ppa:chris-lea/node.js
sudo apt-get update
sudo apt-get install nodejs

npm install express
"""

# Step 1: Create a sites-pre-enabled directory at /etc/nginx/
print "Creating special pre enabled directory...",
import os

directory = "/etc/nginx/sites-pre-enabled"
#directory = "C:\\temp\\lol"
if not os.path.exists(directory):
    os.makedirs(directory)
print "SUCCESS"
    
# Step 2: Copy plugnhost site definition file to pre enabled sites directory
print "Copying site definition file...",
import shutil

file_dir = os.path.dirname(__file__)
print file_dir
filename = os.path.join(dir, '/plugnhost')
print filename
shutil.copy2(filename, directory)
print "SUUCESS"

# Step 3: Edit the nginx.conf file to include pre-enabled sites at the top of
#         the http scope
print "Editing nginx.conf file...",
import fileinput

found = False
for line in fileinput.input('test', inplace=1):
    if line.startswith('http {'):
        found = True # Next line will have a preprinted string
    else:
        if found:
            print '\t#Next line allows a upstream site to be added on top of http scope'
            print "\tinclude /etc/nginx/sites-pre-enabled/*;"
        found = False
    print line,
print "SUCCESS"