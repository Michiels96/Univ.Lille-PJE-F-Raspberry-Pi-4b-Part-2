# coding: utf-8

import socket
import sys

# path à utiliser pour le raspberry pi 
#VIDEO_PATH = "/media/usb0/record/"
VIDEO_PATH = "/root/record_sample/"


class Client():

    def __init__(self, filename):
        ## cette variable transmet la valeur '000' au serveur pour lui indiquer que le client a bien reçu ce que le serveur lui a envoyé, 
        ## ceci permet d'avoir une architecture synchrone 
        self.OkCode = "000"
        self.argFilename = filename

    def statCommandResponse(self):
        readyForSendingFilename = (s.recv(1024)).decode('utf-8')
        if readyForSendingFilename != "OkFilename":
            print("\tServeur n'est pas prêt à recevoir filename\n")
            return

        s.sendall(self.argFilename.encode('utf-8'))
        fileExists = (s.recv(1024)).decode('utf-8')
        if fileExists != "Ok":
            print(fileExists,"\n")
            s.sendall(self.OkCode.encode())
        else:
            s.sendall(self.OkCode.encode())
            #reception des statistiques
            stats = (s.recv(1024)).decode('utf-8')
            print("\tPropriétés du fichier '", self.argFilename,"':")
            print(stats)
            s.sendall(self.OkCode.encode())

    def main(self):
        listOption = "5"
        s.sendall(listOption.encode())
        #reception de l'action demandée
        paquet = s.recv(1024)
        serverResponse = paquet.decode()

        if serverResponse == "Ok5":
            s.sendall(self.OkCode.encode())
            self.statCommandResponse()
        else:
            #erreur reçue du serveur
            print(serverResponse,"\n")
            s.sendall(self.OkCode.encode())


#récupérer l'addr ip, le port et les arguments
ip = sys.argv[1]
port = int(sys.argv[2])
argFilename = str(sys.argv[3])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect(("127.0.0.1", 8080))
s.connect((ip, port))

newClient = Client(argFilename)
newClient.main()