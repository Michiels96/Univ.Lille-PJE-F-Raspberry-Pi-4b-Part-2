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

    def readCommandResponse(self):
        readyForSendingSize = (s.recv(1024)).decode('utf-8')
        if readyForSendingSize != "OkSize":
            print("\tServeur n'est pas prêt à recevoir <size>\n\n")
            return
        size = 0
        while True:
            try:
                print("Introduisez <size>:")
                size = input()
                size = int(size)
                if size == '':
                    raise ValueError
                elif size < 1:
                    print("Erreur, <size> trop petit")
                else:
                    break
            except:
                print("\tErreur, saisie incorrecte! recommencez")
                continue

        s.sendall(str(size).encode())
        #reçoit les N octets du fichier à lire
        NOctetsALire = int((s.recv(1024)).decode('utf-8'))
        s.sendall(self.OkCode.encode())
        buffer = s.recv(NOctetsALire)
        #ecrit les octets dans un fichier dont le nom est demandé au client
        fileNameSaved = ''
        while True:
            try:
                print("Introduisez le nom du fichier qui contiendra les N octets lus: (#copy-NomFichier)")
                fileNameSaved = input()
                if fileNameSaved == '':
                    raise ValueError
                else:
                    break
            except:
                print("\tErreur, saisie incorrecte! recommencez")
                continue
        subprocess.run(["python3", "clientFs.py", fileNameSaved.encode('utf-8'), buffer, "fuseDir"]) # lance le script clientFs pour créer le système de fichier dans le dossier fuseDir
        s.sendall(self.OkCode.encode())
        print("\tSystème de fichier '", fileNameSaved,"' monté \n\n")

    def main(self):
        listOption = "2"
        s.sendall(listOption.encode())
        #reception de l'action demandée
        paquet = s.recv(1024)
        serverResponse = paquet.decode()


        if serverResponse == "Ok2":
            s.sendall(self.OkCode.encode())
            self.readCommandResponse()
        else:
            #erreur reçue du serveur
            print(serverResponse,"\n")
            s.sendall(self.OkCode.encode())


#récupérer l'addr ip, le port et les arguments
ip = sys.argv[1]
port = int(sys.argv[2])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect(("127.0.0.1", 8080))
s.connect((ip, port))

newClient = Client()
newClient.main()
