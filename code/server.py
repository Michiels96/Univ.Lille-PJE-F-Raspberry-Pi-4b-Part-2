# coding: utf-8 

import socket
import threading
import os
import re
import time

# VARIABLES GLOBALES
ERROR_ARRAY = {
    '001': 'choix invalide!', 
    '002': 'Le client n\'a pas confirmé la réception du paquet venant du serveur!',
    '003': 'le client n\'a pas encore ouvert de fichier!',
    '004': 'le client a déjà ouvert un autre fichier!',
    '005': 'le fichier n\'existe pas ou n\'est pas lisible!'
    }
# path à utiliser pour le raspberry pi 
#VIDEO_PATH = "/media/usb0/record/"
VIDEO_PATH = "/root/record_sample/"

clientArrayToCheckFileAlreadyOpen = {}

class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):

        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        self.fileAlreadyOpen = False
        # première fois que le client se connecte au serveur
        if ip not in clientArrayToCheckFileAlreadyOpen:
            clientArrayToCheckFileAlreadyOpen[ip] = False
        self.fileName = ''
        self.fileOpenedId = -1

        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port, ))

    def menu(self):
        # option1 = "1) 'open <filename>' pour ouvrir un fichier passé en paramètre en lecture"
        # option2 = "2) 'read <size>' pour lire le fichier ouvert précédemment \n\t(Uniquement si un fichier a été ouvert précédemment)"
        # option3 = "3) 'close' pour fermer un fichier \n\t(Uniquement si un fichier a été ouvert précédemment)"
        # option4 = "4) 'list' pour afficher l'arborescence des fichiers"
        # option5 = "5) 'stat <filename>' pour afficher les propriétés du fichier passé en paramètre"
        # optionQuit = "'q' pour se déconnecter"
        # display = option1+"\n"+option2+"\n"+option3+"\n"+option4+"\n"+option5+"\n"+optionQuit+"\n"
        #print(display)

        # conversion en bytes pour l'envoi vers le client
        # paquet = bytes(display, 'utf-8')
        # self.clientsocket.sendall(paquet)
        #self.clientsocket.sendall(display.encode('utf-8'))
        
        choix = (self.clientsocket.recv(1024)).decode('utf-8')
        print("RECU du client --> ", choix)

        #switch inexistant en Python
        if choix == '1':
            if clientArrayToCheckFileAlreadyOpen[self.ip] == True:
                display = "\tCODE ERREUR Nr 004: "+ERROR_ARRAY['004']
                print(display)
            else:
                display = "Ok1"

            self.clientsocket.sendall(display.encode('utf-8'))
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                #break
            if clientArrayToCheckFileAlreadyOpen[self.ip] == False:
                self.openCommand()
        elif choix == '2':
            if self.fileAlreadyOpen == False:
                display = "\tCODE ERREUR Nr 003: "+ERROR_ARRAY['003']
                print(display)
            else:
                display = "Ok2"
            
            self.clientsocket.sendall(display.encode('utf-8'))
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                #break
            if self.fileAlreadyOpen == True:
                self.readCommand()
        elif choix == '3':
            if self.fileAlreadyOpen == False:
                display = "\tCODE ERREUR Nr 003: "+ERROR_ARRAY['003']
                print(display)
            else:
                display = "Ok3"

            self.clientsocket.sendall(display.encode('utf-8'))
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                #break
            if self.fileAlreadyOpen == True:
                self.closeCommand()
        elif choix == '4':
            display = "Ok4"
            self.clientsocket.sendall(display.encode('utf-8'))
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                #break
            self.listCommand()
        elif choix == '5':
            #pour cette option, il n'est pas nécessaire d'avoir ouvert préalablement un fichier
            display = "Ok5"
            self.clientsocket.sendall(display.encode('utf-8'))
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                #break
            self.statCommand()
        elif choix == 'q':
            display = "Okq"
            self.clientsocket.sendall(display.encode('utf-8'))
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                #break
        else:
            display = "\tCODE ERREUR Nr 001: "+ERROR_ARRAY['001']
            print(display)
            self.clientsocket.sendall(display.encode('utf-8'))
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                #break

    def openCommand(self):
        print("hello from openCommand()")
        # avertir le client qu'il peut transmettre le nom de fichier a rechercher
        readyForRecieveFilename = "OkFilename"
        self.clientsocket.sendall(readyForRecieveFilename.encode('utf-8'))
        # reçoit le nom de fichier à ouvrir
        fileName = (self.clientsocket.recv(1024)).decode('utf-8')
        if(os.path.exists(VIDEO_PATH+fileName) == False):
            print("\tFichier ", fileName, "inexistant")
            noFile = "noFile"
            self.clientsocket.sendall(noFile.encode('utf-8'))

            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                return
        else:
            print("\tOuverture du fichier: ", fileName, "...")
            # on sauvegarde le nom de fichier par thread client pour pouvoir le lire ensuite lors de l'exécution de la commande 'read' de celui-ci
            self.fileName = fileName
            self.fileOpenedId = open(VIDEO_PATH+fileName, 'rb')
            clientArrayToCheckFileAlreadyOpen[self.ip] = True
            fileOpened = "Ok"
            self.clientsocket.sendall(fileOpened.encode('utf-8'))
            
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                return

    def readCommand(self):
        print("hello from readCommand()")
        # avertir le client qu'il peut transmettre la taille d'octets à lire
        readyForRecieveSize = "OkSize"
        self.clientsocket.sendall(readyForRecieveSize.encode('utf-8'))
        # reçoit la taille d'octets à lire
        size = int((self.clientsocket.recv(1024)).decode('utf-8'))
        
        #si la taille du fichier est plus grand que le nombre d'octets que le client à demandé à lire, 
        #on lui renvera size-1 octets (car la consigne demande que les N octets envoyés soient non-négatif et inférieur à <size>)
        if os.path.getsize(VIDEO_PATH+self.fileName) >= size:
            print("\ttaille du fichier plus grand que <size> donné")
            #doit envoyer les N octets à lire
            NOctetsALire = str((size-1))
            self.clientsocket.sendall(NOctetsALire.encode('utf-8'))
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                return
            #doit envoyer les N octets du fichier
            buffer = self.fileOpenedId.read(size-1)
            #pas besoin d'encode(), on transfert les octets en binaire
            self.clientsocket.sendall(buffer)
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                return
        else:
            print("\ttaille du fichier plus petit que <size> donné")
            #doit envoyer les N octets à lire
            NOctetsALire = os.path.getsize(VIDEO_PATH+self.fileName)
            self.clientsocket.sendall(str(NOctetsALire).encode('utf-8'))
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                return
            #avant de lire le fichier, il faut remettre la position de lecture à sa position de départ
            self.fileOpenedId.seek(0, os.SEEK_SET)
            #doit envoyer les N octets du fichier
            buffer = self.fileOpenedId.read()
            self.clientsocket.sendall(buffer)
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                return

    def closeCommand(self):
        print("hello from closeCommand()")
        self.fileOpenedId.close()
        print("\tFichier '", self.fileName,"' fermé!")
        self.fileAlreadyOpen = False

        fileClosed = "Ok"
        self.clientsocket.sendall(fileClosed.encode('utf-8'))
            
        OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
        if OkCode != "000":
            print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
            return

    def listCommand(self):
        print("hello from listCommand()")
        videoListDisplay = ""
        for f in os.listdir(VIDEO_PATH):
            if not f.startswith('.'):
                videoListDisplay += (f+"\n")
        videoListDisplay += "\n"
        self.clientsocket.sendall(videoListDisplay.encode('utf-8'))
        #vérifier que le client à bien terminé 
        OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
        if OkCode != "000":
            #print("Fatal Error, client hasn't send the end-code to server, \n\tclient-connection will now end\n\tGoodbye dear ", self.ip)
            print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
        
    def statCommand(self):
        print("hello from statCommand()")
        # avertir le client qu'il peut transmettre le nom de fichier a rechercher
        readyForRecieveFilename = "OkFilename"
        self.clientsocket.sendall(readyForRecieveFilename.encode('utf-8'))
        # reçoit le nom de fichier à ouvrir
        fileName = (self.clientsocket.recv(1024)).decode('utf-8')
        if(os.path.exists(VIDEO_PATH+fileName) == False):
            noFile = "\tCODE ERREUR Nr 005: "+ERROR_ARRAY['005']
            print(noFile)
            self.clientsocket.sendall(noFile.encode('utf-8'))

            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                return
        else:
            fileOpened = "Ok"
            self.clientsocket.sendall(fileOpened.encode('utf-8'))
            
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                return

            #envoi des statistiques
            #Taille (en octets)
            bufferSystemResponse = re.search('os\.stat_result\((.+)\)', str(os.stat(VIDEO_PATH+fileName))).group(1).split(", ")
            
            bufferSystemResponseJsonArray = {}
            for i in bufferSystemResponse:
                savedKey = re.search('^(.+)=(.+)', str(i)).group(1)
                savedValue = re.search('^(.+)=(.+)', str(i)).group(2)
                bufferSystemResponseJsonArray[savedKey] = savedValue

            sizeInBytes = bufferSystemResponseJsonArray["st_size"]
            raw_time = int(bufferSystemResponseJsonArray["st_mtime"])
            lastModified = time.ctime(raw_time)
            raw_rights = re.search('([0-9])([0-9])([0-9])$', str(oct(int(bufferSystemResponseJsonArray["st_mode"]))))
            userRights = self.giveTheRight(int(raw_rights.group(1)))
            groupRight = self.giveTheRight(int(raw_rights.group(2)))
            othersRight = self.giveTheRight(int(raw_rights.group(3)))
            #le "-" indique que c'est un fichier et pas un dossier(ce qui est normal)
            fileRightsInOctal = "-"+userRights+groupRight+othersRight
            infoBufferForClient = "\t- taille (en octets): "+sizeInBytes+"\n\t- date de la dernière modification: \n\t\t"+lastModified+"\n\t- droits d’accès: "+fileRightsInOctal+"\n\n"
            self.clientsocket.sendall(infoBufferForClient.encode('utf-8'))
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                return

    def giveTheRight(self, number):
        if number == 4:
            return "r--"
        elif number == 2:
            return "-w-"
        elif number == 1:
            return "--x"
        elif number == 6:
            return "rw-"
        elif number == 5:
            return "r-x"
        elif number == 3:
            return "-wx"
        elif number == 7:
            return "rwx"


    def run(self):
        print("Connexion de %s %s" % (self.ip, self.port, ))
        self.menu()
        print("Client déconnecté...")


tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# "" pour l'HOST permet de recevoir une connexion de n'importe quelle addr IP
tcpsock.bind(("",8080))

while True:
    tcpsock.listen(10)
    print( "En écoute...")
    (clientsocket, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()