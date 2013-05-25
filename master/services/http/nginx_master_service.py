import fileinput, shutil, os
from subprocess import call

NGINX_DIR = "/etc/nginx/"
#NGINX_DIR = "C:/projects/eclipse/plugnhost/master/services/http/"
NGINX_CONFIG_FILE = NGINX_DIR+"nginx.conf.example"

class NginxMasterService(object):
    
    def on_worker_change(self, workers):
        """ Will be run every time the amount of workers for this service
        changes
        """
        print "Rewriting site file... ",
        site_file = NGINX_DIR+"sites-pre-enabled/plugnhost"
        site_file_backup = site_file+"~"
        # Take backup of file
        shutil.copy2(site_file, site_file_backup)
        
        # Attempt to edit nginx site config file
        failed = False
        error = None
        below_tag = False
        for line in fileinput.input(site_file, inplace=1):
            try:
                if "# WORKER NODES START #" in line:
                    below_tag = True # Next line will have a preprinted string
                else:
                    if below_tag:
                        if "server" in line:
                            continue
                        else:
                            for worker in workers:
                                print "\tserver %s:%s;" % (worker.IP, worker.PORT)
                            below_tag = False
                print line,
            except Exception as err:
                failed = True
                error = err
        
        if failed:
            shutil.copy2(site_file_backup, site_file)
            print "ERROR"
            print error
        else:
            print "SUCCESS"
        
        # Delete backup file
        os.remove(site_file_backup)
        
        # Reload nginx config
        call(["service", "nginx", "reload"])
    
    def install(self):
        """ This method should contain a script that installs all dependencies and does
        all local changes for the service to be runnable
        
        """
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
        apk-installas adkasdkasdk ikke pip
        """
        
        # Step 1: Create a sites-pre-enabled directory at /etc/nginx/
        print "Creating special pre enabled directory...",
        import os
        pre_enabled_dir = NGINX_DIR+"sites-pre-enabled"
        if not os.path.exists(pre_enabled_dir):
            os.makedirs(pre_enabled_dir)
        print "SUCCESS"
            
        # Step 2: Copy plugnhost site definition file to pre enabled sites directory
        print "Copying site definition file...",
        import shutil
        
        site_file = os.path.join(os.path.dirname(__file__), 'plugnhost')
        shutil.copy2(site_file, pre_enabled_dir)
        print "SUCCESS"
        
        # Step 3: Edit the nginx.conf file to include pre-enabled sites at the top of
        #         the http scope
        print "Editing nginx.conf file...",
        
        include_string = "include /etc/nginx/sites-pre-enabled/*;"
        if include_string in open(NGINX_CONFIG_FILE).read():
            print "SKIPPED (already done)"
        else:
            found = False
            for line in fileinput.input(NGINX_CONFIG_FILE, inplace=1):
                if line.startswith('http {'):
                    found = True # Next line will have a preprinted string
                else:
                    if found:
                        print "\t#Next line allows a upstream site to be added, has to be on top of http"
                        print "\t"+include_string
                        print "\n"
                    found = False
                print line,
            print "SUCCESS"
            
if __name__ == '__main__':
    NginxMasterService().install()