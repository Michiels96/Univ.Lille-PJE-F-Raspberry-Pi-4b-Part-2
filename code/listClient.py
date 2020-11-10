# coding: utf-8

import socket
import sys

# path à utiliser pour le raspberry pi 
#VIDEO_PATH = "/media/usb0/record/"
VIDEO_PATH = "/root/record_sample/"


class Client():

    def __init__(self):
        ## cette variable transmet la valeur '000' au serveur pour lui indiquer que le client a bien reçu ce que le serveur lui a envoyé, 
        ## ceci permet d'avoir une architecture synchrone 
        self.OkCode = "000"

    def listCommandResponse(self):
        print("Liste de tous les fichiers dans le répertoire:")
        display = (s.recv(1024)).decode('utf-8')
        print(display)
        s.sendall(self.OkCode.encode())

    def main(self):
        listOption = "4"
        s.sendall(listOption.encode())
        #reception de l'action demandée
        paquet = s.recv(1024)
        serverResponse = paquet.decode()

        if serverResponse == "Ok4":
            s.sendall(self.OkCode.encode())
            self.listCommandResponse()
        else:
            #erreur reçue du serveur
            print(serverResponse,"\n")
            s.sendall(self.OkCode.encode())


#récupérer l'addr ip et le port
ip = sys.argv[1]
port = int(sys.argv[2])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect(("127.0.0.1", 8080))
s.connect((ip, port))

newClient = Client()
newClient.main()