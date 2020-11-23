# coding: utf-8

import socket
import re
import sys

# path à utiliser pour le raspberry pi 
#VIDEO_PATH = "/media/usb0/record/"
VIDEO_PATH = "/root/record_sample/"


class Client():

    def __init__(self, filename):
        ## cette variable transmet la valeur '000' au serveur pour lui indiquer que le client a bien reçu ce que le serveur lui a envoyé, 
        ## ceci permet d'avoir une architecture synchrone 
        self.OkCode = "000"
        self.argFilenameToOpen = filename

    def openCommandResponse(self):
        readyForSendingFilename = (s.recv(1024)).decode('utf-8')
        if readyForSendingFilename != "OkFilename":
            print("\tServeur n'est pas prêt à recevoir filename\n")
            return

        s.sendall(self.argFilenameToOpen .encode('utf-8'))
        fileExists = (s.recv(1024)).decode('utf-8')

        if re.search('^\tCODE', fileExists):
            print(fileExists, "\n")
            s.sendall(self.OkCode.encode())
        else:
            print("\t", fileExists,"\n\n")
            s.sendall(self.OkCode.encode())

    def main(self):
        listOption = "1"
        s.sendall(listOption.encode())
        #reception de l'action demandée
        paquet = s.recv(1024)
        serverResponse = paquet.decode()

        if serverResponse == "Ok1":
            s.sendall(self.OkCode.encode())
            self.openCommandResponse()
        else:
            #erreur reçue du serveur
            print(serverResponse,"\n")
            s.sendall(self.OkCode.encode())


#récupérer l'addr ip, le port et les arguments
ip = sys.argv[1]
port = int(sys.argv[2])
argFilenameToOpen = str(sys.argv[3])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect(("127.0.0.1", 8080))
s.connect((ip, port))

newClient = Client(argFilenameToOpen)
newClient.main()