#######################################################################
#
#   Author: Edlin(LIN Junhao) edlinlink@qq.com
#   Date:   Nov. 11,2014
#   University: Honk Kong University Science and Technology
#      
#   Envionment: 
#       Mac OS X 10.9.5
#       Python 2.7.8        
#
#   This is a tiny python webserver. "tinyhttpd" is a C webserver 
#   written by J. David. You can find his source code here:
#   http://tinyhttpd.sourceforge.net/
#
#   It is interesting for me to read his code after 15 years later.
#   However, it makes me more execited to write open source tool.
#
#   "tinypyhttpd" is an tiny websercer which I do not guarantee 
#   anything. Actually there is still many bugs there. But it is good 
#   for new learner to know how the webserver work.
#
#   Please feel free to eamil to me telling your opinion or suggestion
#   about tinypyhttpd.
#
#
#   The file can be distribute under GPL License.
#
#######################################################################
from socket import *
from subprocess import Popen, PIPE
import urllib
import time
import os


########################################################################
#   This function try to setup the socket.
#
#   Parameter: The port to listen. If 'port' equal to 0, dynamicly 
#   allocate one idle port to listen.
#   
#   Return: The socket and the port number.
#
#   The default IP address is 127.0.0.1. You can change to your IP 
#   address if you want to ues it through Internet.
########################################################################
def startup(port):
    httpd = socket(AF_INET, SOCK_STREAM)
    host = "127.0.0.1"

    if port != 0:
        try:
            httpd.bind((host, port))
        except:
            error("bind")
    else:
        for idleport in range(50000, 60000):
            try:
                httpd.bind((host, idleport))
                port = idleport
            except:
                continue;   
    return httpd, port
     

########################################################################
#   A request has caused a accept() on the server port to return.
#
#   Parameter: The socket connected to the client.
#
#   Return: The html page
########################################################################
def accept_request(client):
    request = client.recv(1024)
    request = urllib.unquote(request).split('\r\n')
    method, url, version = request[0].split(' ')
    print method, url, version

    if method == "GET":
        cgi = False
    elif method == "POST":
        cgi = True
        query_string = request[request.index("")+1]

    path = "htdocs" + url
    if url == "/":
        path += "index.html"

    if cgi == False:
        serve_file(client, path)
    else:
        execute_cgi(client, path, method, query_string)


########################################################################
#   Execute the CGI script.
#
#   Parameter: 
#       The socket connect to the client;
#       The file path;
#       The method "GET" or "POST";
#       The query_string RGB code, eg: #FF0000.
########################################################################
def execute_cgi(client, path, method, query_string):
    try:
        cgi_input = query_string.split("=")
    except:
        client.close
        return 

    headers(client)
    cgi = Popen(path, stdin=PIPE, stdout=PIPE)
    cgi.stdin.write(cgi_input[1]+"\n")
    cgi_output = cgi.stdout.read()
    client.send(cgi_output)
    client.close()



########################################################################
#   Send regular file to client. 
#
#   Parameter: The socket connect to the client.
#              The file path 
#
#########################################################################
def serve_file(client, filename):
    if not os.path.exists(filename):
        print "[NO file]:", filename
        not_found(client)
        client.close()
    else:
        resource = open(filename, "r")
        headers(client)
        buffer = "".join(resource.readlines())
        client.send(buffer)
        resource.close()
        client.close()


#########################################################################
#   Return the informational HTTP headers about the file
#
#   Parameter: The socket to print the header on the file
#########################################################################
def headers(client):
    buffer = "HTTP/1.0 200 OK\r\n"
    buffer += "Server: tinypyhttpd/0.1.0\r\n"
    buffer += time.strftime("Date: %a, %d %b %Y %H:%M:%S GMT\r\n", time.gmtime())
    buffer += "Content-Type: text/html; charset=UTF-8\r\n"
    buffer += "\r\n"
    client.send(buffer)


#########################################################################
#   Reply the 404 page telling no request file
#
#   Parameter: The socket connected to the client
#########################################################################
def not_found(client):
    buffer = "HTTP/1.0 404 Not Found\r\n"
    buffer += "Server: tinypyhttpd/0.1.0\r\n"
    buffer += time.strftime("Date: %a, %d %b %Y %H:%M:%S GMT\r\n", time.gmtime())
    buffer += "Content-Type: text/html; charset=UTF-8\r\n"
    buffer += "\r\n"
    buffer += "<head><body><H>404 Not Found.</body></head>\r\n"
    client.send(buffer)
   

if __name__ == "__main__":
    port = 0
    server_socket, port = startup(port)
    print "httpd running on port", port

    server_socket.listen(5)
    while 1:
        client_socket, client_address = server_socket.accept()
        print "=> [Client From]:", client_address
        accept_request(client_socket)

