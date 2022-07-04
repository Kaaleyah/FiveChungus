# BROADCASTER FILE

from os.path import splitext
from socket import *
from time import *
import json
import math
import os

import sys
import shutil

toBeAnnounced = sys.argv[1]

def announce(broadcastSocket, message):
    broadcastSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    broadcastSocket.connect(('192.168.1.255', 5001))

    print(message + "\n")

    broadcastSocket.send(message.encode())

# END OF announce

def splitFile(fileName):
    filePath = "../files/" + fileName

    content = splitext(fileName)[0]

    c = os.path.getsize(filePath)
    print(f"File Size: {c} bytes")
    CHUNK_SIZE = math.ceil(math.ceil(c)/5)
    print(f"Chunks Size: {CHUNK_SIZE} bytes\n")


    index = 1
    with open(filePath, 'rb') as infile:
        chunk = infile.read(int(CHUNK_SIZE))
        while chunk:
            chunkName = content + '_' + str(index)

            chunkPath = "../chunks/" + chunkName;

            with open(chunkPath,'wb+') as chunk_file:
                chunk_file.write(chunk)
            index += 1
            chunk = infile.read(int(CHUNK_SIZE))
    chunk_file.close()

# END OF splitFile

###      MAIN      ###

if (not os.path.isfile("../files/" + toBeAnnounced)):
    print("The file does not exist!")    
    sys.exit()

splitFile(toBeAnnounced)

chunksJSON = {
    "chunks": os.listdir("../chunks/")
}

chunksJSON = json.dumps(chunksJSON);

print(f"Starting to broadcast 5 chunks of: {toBeAnnounced}")

chunksJSON = {
    "chunks": os.listdir("../chunks/")
}

chunksJSON = json.dumps(chunksJSON);

broadcastSocket = socket(AF_INET, SOCK_DGRAM)

announce(broadcastSocket, chunksJSON)


copyPath = "../files/" + toBeAnnounced
pastePath = "../announcedFiles/" + toBeAnnounced

shutil.copyfile(copyPath, pastePath)

sys.sdout.flush()

#   ♪The soul of this sick bulwark forever and ever♪