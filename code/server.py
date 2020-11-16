# coding: utf-8 

import socket
import threading
import os
import re
import time
import sys

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

clientArrayOpenedFileName = {}
clientArrayOpenedFileNameId = {}

class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):

        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        # première fois que le client se connecte au serveur
        self.lock.acquire()
        if ip not in clientArrayOpenedFileName:
            clientArrayOpenedFileName[ip] = 'null'
        self.lock.release()
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port, ))

    def menu(self):     
        choix = (self.clientsocket.recv(1024)).decode('utf-8')
        print("RECU du client --> ", choix)

        #switch inexistant en Python
        if choix == '1':
            self.lock.acquire()
            if clientArrayOpenedFileName[self.ip] != 'null':
                display = "\tCODE ERREUR Nr 004: "+ERROR_ARRAY['004']
                print(display)
            else:
                display = "Ok1"
            self.lock.release()

            self.clientsocket.sendall(display.encode('utf-8'))
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
            self.lock.acquire()
            if clientArrayOpenedFileName[self.ip] == 'null':
                self.lock.release()
                self.openCommand()
            else:
                self.lock.release()
        elif choix == '2':
            self.lock.acquire()
            if clientArrayOpenedFileName[self.ip] == 'null':
                display = "\tCODE ERREUR Nr 003: "+ERROR_ARRAY['003']
                print(display)
            else:
                display = "Ok2"
            self.lock.release()
            
            self.clientsocket.sendall(display.encode('utf-8'))
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
            self.lock.acquire()
            if clientArrayOpenedFileName[self.ip] != 'null':
                self.lock.release()
                self.readCommand()
            else:
                self.lock.release()
        elif choix == '3':
            self.lock.acquire()
            if clientArrayOpenedFileName[self.ip] == 'null':
                display = "\tCODE ERREUR Nr 003: "+ERROR_ARRAY['003']
                print(display)
            else:
                display = "Ok3"
            self.lock.release()

            self.clientsocket.sendall(display.encode('utf-8'))
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
            self.lock.acquire()
            if clientArrayOpenedFileName[self.ip] != 'null':
                self.lock.release()
                self.closeCommand()
            else:
                self.lock.release()
        elif choix == '4':
            display = "Ok4"
            self.clientsocket.sendall(display.encode('utf-8'))
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
            self.listCommand()
        elif choix == '5':
            #pour cette option, il n'est pas nécessaire d'avoir ouvert préalablement un fichier
            display = "Ok5"
            self.clientsocket.sendall(display.encode('utf-8'))
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
            self.statCommand()
        elif choix == 'q':
            display = "Okq"
            self.clientsocket.sendall(display.encode('utf-8'))
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
        else:
            display = "\tCODE ERREUR Nr 001: "+ERROR_ARRAY['001']
            print(display)
            self.clientsocket.sendall(display.encode('utf-8'))
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])

    def openCommand(self):
        print("hello from openCommand()")
        # avertir le client qu'il peut transmettre le nom de fichier a rechercher
        readyForRecieveFilename = "OkFilename"
        self.clientsocket.sendall(readyForRecieveFilename.encode('utf-8'))
        # reçoit le nom de fichier à ouvrir
        fileName = (self.clientsocket.recv(1024)).decode('utf-8')
        if(os.path.exists(VIDEO_PATH+fileName) == False):
            print("\tFichier ", fileName, "inexistant")
            display = "\tCODE ERREUR Nr 005: "+ERROR_ARRAY['005']
            self.clientsocket.sendall(display.encode('utf-8'))

            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                return
        else:
            print("\tOuverture du fichier: ", fileName, "...")
            self.lock.acquire()
            clientArrayOpenedFileName[self.ip] = fileName
            clientArrayOpenedFileNameId[self.ip] = open(VIDEO_PATH+fileName, 'rb')
            self.lock.release()
            fileOpened = "Ok"
            self.clientsocket.sendall(fileOpened.encode('utf-8'))
            
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                return

    def readCommand(self):
        print("hello from readCommand()")
        self.lock.acquire()
        fileOpenedId = clientArrayOpenedFileNameId[self.ip]
        self.lock.release()
        # avertir le client qu'il peut transmettre la taille d'octets à lire
        readyForRecieveSize = "OkSize"
        self.clientsocket.sendall(readyForRecieveSize.encode('utf-8'))
        # reçoit la taille d'octets à lire
        size = int((self.clientsocket.recv(1024)).decode('utf-8'))
        
        #si la taille du fichier est plus grand que le nombre d'octets que le client à demandé à lire, 
        #on lui renvera size-1 octets (car la consigne demande que les N octets envoyés soient non-négatif et inférieur à <size>)
        self.lock.acquire()
        if os.path.getsize(VIDEO_PATH+clientArrayOpenedFileName[self.ip]) >= size:
            self.lock.release()
            print("\ttaille du fichier plus grand que <size> donné")
            #doit envoyer les N octets à lire
            NOctetsALire = str((size-1))
            self.clientsocket.sendall(NOctetsALire.encode('utf-8'))
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                return
            #doit envoyer les N octets du fichier
            buffer = fileOpenedId.read(size-1)
            #pas besoin d'encode(), on transfert les octets en binaire
            self.clientsocket.sendall(buffer)
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                return
        else:
            self.lock.release()
            print("\ttaille du fichier plus petit que <size> donné")
            #doit envoyer les N octets à lire
            self.lock.acquire()
            NOctetsALire = os.path.getsize(VIDEO_PATH+clientArrayOpenedFileName[self.ip])
            self.lock.release()
            self.clientsocket.sendall(str(NOctetsALire).encode('utf-8'))
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                return
            #avant de lire le fichier, il faut remettre la position de lecture à sa position de départ
            fileOpenedId.seek(0, os.SEEK_SET)
            #doit envoyer les N octets du fichier
            buffer = fileOpenedId.read()
            self.clientsocket.sendall(buffer)
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                return

    def closeCommand(self):
        print("hello from closeCommand()")
        self.lock.acquire()
        clientArrayOpenedFileNameId[self.ip].close()
        print("\tFichier '", clientArrayOpenedFileName[self.ip],"' fermé!")
        clientArrayOpenedFileNameId[self.ip] = ''
        clientArrayOpenedFileName[self.ip] = 'null'
        self.lock.release()
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
        self.lock.acquire()
        print("\t",clientArrayOpenedFileName)
        print("\t",clientArrayOpenedFileNameId)
        self.lock.release()
        
    def statCommand(self):
        print("hello from statCommand()")
        # avertir le client qu'il peut transmettre le nom de fichier à rechercher
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
port = int(sys.argv[1])
tcpsock.bind(("",port))

while True:
    tcpsock.listen(10)
    print( "En écoute...")
    (clientsocket, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()