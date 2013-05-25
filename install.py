import sys
import settings

def main():
    if len(sys.argv) == 2:
        install_level = sys.argv[1]
        if install_level == "master":
            install("Master")
        elif install_level == "worker":
            install("Worker")
        elif install_level == "full":
            install("Master")
            install("Worker")
        else:
            print "Bad installation type, use master, worker or full"
    else:
        print "Bad amount of arguments, correct useage: "
        print "\n\tpython install.py master"
        print "\n\tpython install.py worker"
        print "\n\tpython install.py full"

def install(level):
    install_level_str = level+"Class"
    for service_name in settings.SERVICES:
        path_class = settings.SERVICES[service_name][install_level_str].rsplit(".", 1)
        exec ("from %s import %s" % (path_class[0], path_class[1]))
        service = eval(path_class[1]+"")
        service().install()
        
if __name__ == '__main__':
    main()