# DOWNLOADER FILE

from socket import *
import os
import json
from datetime import datetime
from tqdm import tqdm

import sys

requestedFile = sys.argv[1]

sys.stderr.flush()

def log(chunkName, reqIP):
    downloadLog = open("../engine/downloadLog.txt", "a")
    timeStamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    microSecond = datetime.now().strftime("%f")[0:2]
    timeStamp += f":{microSecond}"

    downloadLog.write(f"{chunkName}  |  {timeStamp}  |  {reqIP} \n")

# END OF log

def chunkChecker(chunkName, chunkArr):
    for x in chunkArr:
        if (chunkName == x):
            return True

    return False

# END OF chunkChecker

def chunkMerger(fileNameWext):
    filePath = '../files/'+ fileNameWext

    fileNameWOext = os.path.splitext(fileNameWext)[0]

    chunkListFinal = []

    for i in range(1, 6):
        
        chunkListFinal.append(f"{fileNameWOext}_{i}")

    with open(filePath, 'wb') as outfile: 

        for chunk in chunkListFinal: 

            chunkPath = '../chunks/' + chunk

            with open(chunkPath, 'rb') as infile: 
                outfile.write(infile.read() )

            infile.close()          

# END OF chunkMerger

def parseChunks(fileName, reqIP):

    requestedChunks = []

    for chunkIndex in contentDictionary[reqIP]:
        
        chunk = chunkIndex.split('_')[0]
        
        if(chunk == fileName):

            requestedChunks.append(chunkIndex)
            
    return requestedChunks

# END OF parseChunks

def sendChunks(chunkListSC, remainingChunksSC, currentIP):

    FILE_PORT = 8000

    for request in chunkListSC:
            
            if request in remainingChunksSC:

                downloadSocket= socket(AF_INET, SOCK_STREAM)

                try:
                    downloadSocket.settimeout(20)   #Wait for 20 seconds
                    downloadSocket.connect((currentIP, FILE_PORT))
                    downloadSocket.settimeout(None)
                except:
                    print("\n" + currentIP + " is offline!")
                    return 0

                requestJSON = {
                    'requested_content': request
                }

                requestJSON= json.dumps(requestJSON)
                downloadSocket.send(requestJSON.encode())

                requestPath = "../chunks/" + request
                
                with open(requestPath, "wb") as fileWriter: # START RECEIVING FILE

                    while True:
                        bytesRead = downloadSocket.recv(1024)

                        if not bytesRead:
                            break   # END RECEIVING FILE

                        fileWriter.write(bytesRead)
                        
                fileSize = os.path.getsize(requestPath)      

                if (fileSize == 0):
                    os.remove(requestPath)
                    print("\nFailed to download " + request +   " from " + currentIP)
                else:
                    remainingChunksSC.remove(request)
                    log(request, currentIP)

                downloadSocket.close()

# END OF sendChunks

##   MAIN   ##

with open('../engine/contentDictionary.txt') as dictionaryFile:
        contentDictionary = json.load(dictionaryFile)

#requestedFile = input("Please input the file you wish to download: ")

fileName = os.path.splitext(requestedFile)[0]

remainingChunks = []

for i in range(1, 6):
    
    remainingChunks.append(f"{fileName}_{i}")

for candidateIP in contentDictionary:

    chunkList = parseChunks(fileName, candidateIP)

    sendChunks(chunkList, remainingChunks, candidateIP)    

    if not remainingChunks:
        chunkMerger(requestedFile)

        break

if remainingChunks:
    print("\n")
    for x in remainingChunks:

        print(f"Failed to download chunk {x} from any peer(s).")
else:
    print(f"\nDownloaded {requestedFile} successfully!\n")

sys.stdout.flush()

# There was a time that the pieces fit, but I watched them fall away.
# Mildewed and smoldering, strangled by our coveting
# I've done the math enough to know the dangers of our second guessing
# Doomed to crumble unless we grow, and strengthen our communication.

# Schism - TOOL