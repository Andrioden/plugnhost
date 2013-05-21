# Step 1: Create a sites-pre-enabled directory at /etc/nginx/
import os

directory = "/etc/nginx/sites-pre-enabled"
if not os.path.exists(directory):
    os.makedirs(directory)
    
# Step 2: Copy plugnhost site defenition file to pre enabled sites directory
import shutil

shutil.copy2('plugnhost', directory)

# Step 3: Edit the nginx.conf file to include pre-enabled sites at the top of
#         the http scope
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