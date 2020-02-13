import os
import time
from socket import *
import sys
import select
import threading
import signal


def signal_handler(sig, frame):
    print('stop thread')
    x.stop()
    sys.exit(0)



basepath = 'folder/'

def send(frm, to, tck):
    s = socket(AF_INET,SOCK_DGRAM)
    host ="127.0.0.1."
    port = 9999
    buf =1024
    addr = (host,port)

    file_name=basepath+frm+"_"+to+"_"+tck

    s.sendto(file_name,addr)

    f=open(file_name,"rb")
    data = f.read(buf)
    while (data):
        if(s.sendto(data,addr)):
            print("sending ...")
            data = f.read(buf)
    s.close()
    f.close()

def listen():
    host="0.0.0.0"
    port = 9999
    s = socket(AF_INET,SOCK_DGRAM)
    s.bind((host,port))

    addr = (host,port)
    buf=1024

    data,addr = s.recvfrom(buf)
    print("Received File:",data.strip())
    f = open(data.strip(),'wb')

    data,addr = s.recvfrom(buf)
    try:
        while(data):
            f.write(data)
            s.settimeout(2)
            data,addr = s.recvfrom(buf)
    except timeout:
        f.close()
        s.close()
        print("File Downloaded")




snd = False
print(len(sys.argv))
if len(sys.argv) > 1 and sys.argv[1]=="send":
    snd = True
else:
    x = threading.Thread(target=listen)
    #x.start()

signal.signal(signal.SIGINT, signal_handler)


while(True):
    for entry in os.listdir(basepath):
        if os.path.isfile(os.path.join(basepath, entry)):
            frm, to, tick = entry.split("_")
            print("From: "+frm+" To: "+to)
            if snd==True:
                send(frm, to, tick)
            


    time.sleep(5)        
        
