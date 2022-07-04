# UPLOADER FILE

from socket import *
import json
from datetime import datetime
import os

def log(chunkName, reqIP):
    print("Uploaded " + chunkName + " to " + reqIP)
    uploadLog = open("../engine/uploadLog.txt", "a")
    timeStamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    microSecond = datetime.now().strftime("%f")[0:2]
    timeStamp += f":{microSecond}"

    uploadLog.write(f"{chunkName}  |  {timeStamp}  |  {reqIP} \n")

# END OF log

def chunkChecker(chunkName, chunkArr):
    for x in chunkArr:
        if (chunkName == x):
            return True
            
    return False
    
# END OF chunkChecker

def sendChunks(socketUpload):
    for x in range(5):
        connectionSocket, address = socketUpload.accept();
        requesterIP = address[0]
    
        while 1:
            try:
                msg = connectionSocket.recv(1024)
                requestedChunk = json.loads(msg)["requested_content"]
                
                break
            except ValueError:
                print("Invalid request!")
            except ConnectionResetError:
               return 0

        requestedPath = "../chunks/" + requestedChunk;

        if (os.path.isfile(requestedPath)):

            with open(requestedPath, "rb") as file:
                while True:
                    bytesRead = file.read(1024)

                    if not bytesRead:
                        break

                    connectionSocket.sendall(bytesRead)

            log(requestedChunk, requesterIP)

        connectionSocket.close()

# END OF sendChunks


###    MAIN    ###

uploadSocket = socket(AF_INET, SOCK_STREAM)
filePort = 8000

uploadSocket.bind(('', filePort))

chunkList = os.listdir("../chunks/")

while 1:
    uploadSocket.listen(1)
    print("Listening for requests")

    sendChunks(uploadSocket)

#   ♪ Ba-ba-biddly-ba-ba-ba-ba, ba-ba-ba-ba-ba-ba-ba ♪
#   ♪ We are Number One ♪
#   ♪ Hey! ♪

#   Tribute to Stefán Karl Stefánsson