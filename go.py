import sys, os
import settings
from subprocess import call
import pickle

here_path = os.path.dirname(__file__)
INSTALLED_LIST_FILE_PATH = ".plugged"

def main():
    if 1 < len(sys.argv) < 4:
        installed = _load_or_create_installed()
        go_as = sys.argv[1]
        install_file_path = os.path.join(here_path, 'install.py')
        if go_as == "master":
            if not _is_all_services_installed_for(installed, "master"):
                print "Installing master services..."
                installed['master_services'] = [s for s in settings.SERVICES]
                call("python %s master" % install_file_path, shell=True)
                pickle.dump(installed, open(INSTALLED_LIST_FILE_PATH, "wb"))
                print "...Successfully installed master services"
            print "Starting master services..."
            master_file_path = os.path.join(here_path, "master" "master_node.py")
            call("python %s" % master_file_path)
        elif go_as == "workfor":
            if len(sys.argv) !=3:
                print_help()
                return
            else:
                go_host = sys.argv[2]
                if not _is_all_services_installed_for(installed, "worker"):
                    print "Installing worker services..."
                    installed['worker_services'] = [s for s in settings.SERVICES]
                    call("python %s worker" % install_file_path, shell=True)
                    pickle.dump(installed, open(INSTALLED_LIST_FILE_PATH, "wb"))
                    print "...Successfully installed worker services"
                print "Starting worker services..."
                worker_file_path = os.path.join(here_path, "worker", "worker_node.py")
                call("python %s %s" % (worker_file_path, go_host))
        else:
            print_help()
            return
    else:
        print_help()
        
        
def _load_or_create_installed():
    # Load or create a new installed dictionary
    if os.path.isfile(INSTALLED_LIST_FILE_PATH):
        installed = pickle.load( open( INSTALLED_LIST_FILE_PATH, "rb" ) )
    else:
        installed = {'master_services': [],
                     'worker_services': []}
    return installed
        
def _is_all_services_installed_for(installed, level):
    """Check if all services are installed for given level"""
    for service_name in settings.SERVICES:
        if not service_name in installed[level+"_services"]:
            return False
    return True


def print_help():
    print "Bad amount of arguments or argument name, correct useage: "
    print "\n\tpython go.py master"
    print "\n\tpython go.py workfor [host]"
        
if __name__ == '__main__':
    #print [s for s in settings.SERVICES]
    #pickle.dump(["ok", "no"], open(INSTALLED_LIST_FILE_PATH, "wb"))
    #print pickle.load( open( INSTALLED_LIST_FILE_PATH, "rb" ) )
    #installed = pickle.dumps(["ok", "no"])
    main()