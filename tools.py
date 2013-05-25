import socket
import tempfile
import os

def get_open_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("",0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port

def download(base_url, file_name):
    from urllib2 import Request, urlopen, URLError, HTTPError
    
    #create the url and the request
    url = base_url + file_name
    req = Request(url)
    
    # Open the url
    try:
        f = urlopen(req)
        print "downloading " + url
        
        # Open our local file for writing
        download_file_path = os.path.join(tempfile.gettempdir(), file_name)
        local_file = open(download_file_path, "wb")
        #Write to our local file
        local_file.write(f.read())
        local_file.close()
        return download_file_path
        
    #handle errors
    except HTTPError, e:
        print "HTTP Error:",e.code , url
    except URLError, e:
        print "URL Error:",e.reason , url