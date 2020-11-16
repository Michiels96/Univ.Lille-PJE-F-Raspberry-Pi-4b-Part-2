# coding: utf-8

import socket

# path à utiliser pour le raspberry pi 
#VIDEO_PATH = "/media/usb0/record/"
VIDEO_PATH = "/root/record_sample/"


class Client():

    def __init__(self):
        ## cette variable transmet la valeur '000' au serveur pour lui indiquer que le client a bien reçu ce que le serveur lui a envoyé, 
        ## ceci permet d'avoir une architecture synchrone 
        self.OkCode = "000"
        self.fileNameSaved = ''

    def openCommandResponse(self):
        readyForSendingFilename = (s.recv(1024)).decode('utf-8')
        if readyForSendingFilename != "OkFilename":
            print("\tServeur n'est pas prêt à recevoir filename\n")
            return
        fileName = ''
        while True:
            try:
                print("Introduisez le nom du fichier à ouvrir: ")
                fileName = input()
                if fileName == '':
                    raise ValueError
                else:
                    break
            except:
                print("\tErreur, saisie incorrecte! recommencez")
                continue

        s.sendall(fileName.encode('utf-8'))
        fileExists = (s.recv(1024)).decode('utf-8')
        if fileExists == "noFile":
            print("\tErreur, le fichier n'existe pas ou n'est pas lisible\n")
            s.sendall(self.OkCode.encode())
        else:
            self.fileNameSaved = fileName
            print("\tFichier '",fileName,"' ouvert!\n\n")
            s.sendall(self.OkCode.encode())

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
        #ecrit les octets dans un fichier
        with open(VIDEO_PATH+"copy-"+self.fileNameSaved, 'wb') as fileOpenedId:
            fileOpenedId.write(buffer)
        s.sendall(self.OkCode.encode())
        print("\tFichier '", self.fileNameSaved,"' lu!\n\n")

    def closeCommandResponse(self):
        fileClosed = (s.recv(1024)).decode('utf-8')
        if fileClosed != "Ok":
            print("\tServeur n'a pas su fermer le fichier '", self.fileNameSaved,"'\n")
            return
        else:
            print("\tLe Fichier '", self.fileNameSaved,"' a correctement été fermé!\n\n")
            self.fileNameSaved = ''
            s.sendall(self.OkCode.encode())


    def listCommandResponse(self):
        print("Liste de tous les fichiers dans le répertoire:")
        display = (s.recv(1024)).decode('utf-8')
        print(display)
        s.sendall(self.OkCode.encode())

    def statCommandResponse(self):
        readyForSendingFilename = (s.recv(1024)).decode('utf-8')
        if readyForSendingFilename != "OkFilename":
            print("\tServeur n'est pas prêt à recevoir filename\n")
            return
        fileName = ''
        while True:
            try:
                print("Introduisez le nom du fichier à ouvrir pour en récupérer les statistiques: ")
                fileName = input()
                if fileName == '':
                    raise ValueError
                else:
                    break
            except:
                print("\tErreur, saisie incorrecte! recommencez")
                continue

        s.sendall(fileName.encode('utf-8'))
        fileExists = (s.recv(1024)).decode('utf-8')
        if fileExists != "Ok":
            print(fileExists,"\n")
            s.sendall(self.OkCode.encode())
        else:
            s.sendall(self.OkCode.encode())
            #reception des statistiques
            stats = (s.recv(1024)).decode('utf-8')
            print("\tPropriétés du fichier '", fileName,"':")
            print(stats)
            s.sendall(self.OkCode.encode())

    def main(self):
        #reception du menu
        choix = ''
        while choix != "q":
            menu = s.recv(1024)
            print(menu.decode())

            while True:
                try:
                    print("choisissez: ")
                    choix = input()
                    if choix == '':
                        raise ValueError
                    else:
                        break
                except:
                    print("Erreur, saisie incorrecte!")
                    continue
                    
            #envois de la reponse
            s.sendall(choix.encode())
            #reception de l'action demandée
            paquet = s.recv(1024)
            serverResponse = paquet.decode()
            #print("Recu -->", serverResponse, "\n")

            if serverResponse == "Ok1":
                s.sendall(self.OkCode.encode())
                self.openCommandResponse()
            elif serverResponse == "Ok2":
                s.sendall(self.OkCode.encode())
                self.readCommandResponse()
            elif serverResponse == "Ok3":
                s.sendall(self.OkCode.encode())
                self.closeCommandResponse()
            elif serverResponse == "Ok4":
                s.sendall(self.OkCode.encode())
                self.listCommandResponse()
            elif serverResponse == "Ok5":
                s.sendall(self.OkCode.encode())
                self.statCommandResponse()
            elif serverResponse == "Okq":
                s.sendall(self.OkCode.encode())
                break
            else:
                #erreur reçue du serveur
                print(serverResponse,"\n")
                s.sendall(self.OkCode.encode())



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 8080))

newClient = Client()
newClient.main()