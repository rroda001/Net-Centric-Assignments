# TCPServer.py
# TCPServer.py



# Week Four Submission. HTTP GET Request of an Existing File. Used Professor Downey's Provided Code as a Start Point
from socket import socket, SOCK_STREAM, AF_INET
import os, time, datetime
# Create a TCP socket
# Notice the use of SOCK_STREAM for TCP packets
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 1985
# Assign IP address and port number to socket
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print "Interrupt with CTRL-C"
while True:
    try:
        connectionSocket, addr = serverSocket.accept()
        print "Connection from %s port %s" % addr
        # Receive the client packet
        message = connectionSocket.recv(2048)
        print "Original message from client: ", message
        # Capitalize the message from the client
        filename = message.split()[1].partition("/")[2]
        print "File requested: %s" % filename
        if "If-Modified-Since:" in message and os.path.isfile(filename):
            clientDate = message.partition("If-Modified-Since: ")[2]
            clientDate = time.mktime(datetime.datetime.strptime(clientDate, "%a, %d %b %Y %X %Z").timetuple())
            print "Unix Date of Client File: %s" % clientDate
            serverDate = os.path.getmtime(filename)
            print "Unix Date of Servers File: %s" % serverDate
            if serverDate <= clientDate:
                header = "HTTP/1.1 304 Not Modified\r\n"
                connectionSocket.send(header)
                connectionSocket.close()

        if "Accept-Language" in message:
            webpage = "hello.html." + (message.partition("Accept-Language: ")[2].split(",")[1].partition(";")[0])
            header = ("HTTP/1.1 200 OK\r\n"
                      "Content-type: text/html\r\n")
            print "webpage language requested: %s" % webpage
            f = open(webpage,'rb')
            data = f.read()
            size = len(data)
            header = ("HTTP/1.1 200 OK\r\n"
                      "Content-Length: %s \r\n"
                      "Content-Type: text/html; charset=ISO-8859-1\r\n") % size
            connectionSocket.send(header)
            connectionSocket.send(data)
            connectionSocket.close()
        else:
            f = open(filename, 'rb')
            data = f.read()
            size = len(data)
            header = ("HTTP/1.1 200 OK\r\n"
                 "Accept-Ranges: bytes\r\n"
                 "Content-Length: %s \r\n"
                 "Keep-Alive: timeout=10, max=10\r\n"
                 "Connection: Keep-Alive\r\n (or Connection: close)"
                 "Last-Modified: %s"
                 "Content-Type: text/html; charset=ISO-8859-1\r\n" "\r\n") % (size, os.path.getmtime(filename))
            print header
            connectionSocket.send(header)
            connectionSocket.send(data)
            f.close()
            connectionSocket.close()
    except KeyboardInterrupt:
        print "\nInterrupted by CTRL-C"
        break
    except IOError:
        nofile = open("404.html", 'rb')
        data = nofile.read()
        size = len(data)
        header = ("HTTP/1.1 404 Not Found\r\n"
                  "Accept-Ranges: bytes\r\n"
                  "Content-Length: %s \r\n"
                  "Keep-Alive: timeout=10, max=10\r\n"
                  "Connection: Close\r\n"
                  "Content-Type: text/html; charset=ISO-8859-1\r\n" "\r\n") % size
        connectionSocket.send(header)
        connectionSocket.send(data)
        connectionSocket.close()
serverSocket.close()
