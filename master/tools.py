import fileinput, shutil, os, socket
from subprocess import call
from settings import NGINX_DIR

def nginx_reqwrite_site_config(workers):
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
    
def get_open_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("",0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port
    