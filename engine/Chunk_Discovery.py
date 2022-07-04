# DISCOVERY CODE

# We are all chasing the light mate, lookin everywhere to find it, everywhere but within

from socket import *
import json
import os

contentDictionary = {}
dictFile = "../engine/contentDictionary.txt"

if (os.path.getsize(dictFile) != 0):
    with open(dictFile, "r") as inputData:
        contentDictionary = json.load(inputData)

def contentParser(receivedMessage, receivedIP):

    chunkList = json.loads(receivedMessage)["chunks"]

    contentDictionary[receivedIP] = []

    contentDictionary[receivedIP] += chunkList

    with open("../engine/contentDictionary.txt", "w") as outputData:
        json.dump(contentDictionary, outputData)

    return contentDictionary

# END OF CONTENT PARSER

def discover(broadcastSocket):

    print("\nWaiting for a broadcast\n")

    receivedMessage, broadcastedAddress = broadcastSocket.recvfrom(1024)

    broadcastedIP = broadcastedAddress[0]

    print("Received broadcast from " + str(broadcastedIP) + "\n")

    decodedMessage = receivedMessage.decode()

    contentDict = contentParser(decodedMessage, broadcastedIP)

    print(contentDict)

    
# END OF DISCOVER FUNCTION


# MAIN

BROADCAST_RCV_SOCKET = socket(AF_INET, SOCK_DGRAM)
BROADCAST_RCV_SOCKET.bind(('', 5001))

while 1:

    discover(BROADCAST_RCV_SOCKET)