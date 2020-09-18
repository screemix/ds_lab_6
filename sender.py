import socket
import sys
import os

###################### reading the arguments from cli ######################
filename = sys.argv[1]
ip = sys.argv[2]
port = sys.argv[3]

###################### creating socket and file objects ######################
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
f = open(filename, 'rb')
pack = f.read(1024)

############### connecting to receiver, verifying the connection ###############
sk.connect((ip, int(port)))
sk.send(bytes(filename, 'utf-8'))
res = sk.recv(1024)

############### if connection was enstablished, start sending ###############
if res == b'ok':
    i = 1

    ## while we are still able to read from data, there is something we did not send yet ##
    while pack:
        sk.send(pack)
        print(f"Progress: {100 * (i * 1024 / os.path.getsize(filename))}% done", flush=True)
        i += 1
        pack = f.read(1024)
