# coding: utf-8 

import socket
import threading
import os


# VARIABLES GLOBALES
ERROR_ARRAY = {
    '001': 'choix invalide!', 
    '002': 'Le client n\'a pas confirmé la réception du paquet venant du serveur!'
    }
# path à utiliser pour le raspberry pi 
#VIDEO_PATH = "/media/usb0/record/"
VIDEO_PATH = "/root/record_sample/"



class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):

        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port, ))

    def menu(self):
        choix = ""
        while choix != "q":
            option1 = "1) 'open <filename>' pour ouvrir un fichier passé en paramètre en lecture"
            option2 = "2) 'read <size>' pour lire le fichier ouvert précédemment \n\t(Uniquement si un fichier a été ouvert précédemment)"
            option3 = "3) 'close' pour fermer un fichier \n\t(Uniquement si un fichier a été ouvert précédemment)"
            option4 = "4) 'list' pour afficher l'arborescence des fichiers"
            option5 = "5) 'stat <filename>' pour afficher les propriétés du fichier passé en paramètre"
            optionQuit = "'q' pour se déconnecter"
            display = option1+"\n"+option2+"\n"+option3+"\n"+option4+"\n"+option5+"\n"+optionQuit+"\n"
            #print(display)

            # conversion en bytes pour l'envoi vers le client
            # paquet = bytes(display, 'utf-8')
            # self.clientsocket.sendall(paquet)
            self.clientsocket.sendall(display.encode('utf-8'))
            
            choix = (self.clientsocket.recv(1024)).decode('utf-8')
            print("RECU du client --> ", choix)

            #switch inexistant en Python
            if choix == '1':
                display = "Ok1"
                self.clientsocket.sendall(display.encode('utf-8'))
                OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
                if OkCode == "clientAlreadyOpenedAnotherFile":
                    print("Commande 'open' annulée, le client à déjà ouvert un autre fichier")
                elif OkCode != "000":
                    print("CODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                    break
                else:
                    self.openCommand()
            elif choix == '2':
                display = "Ok2"
                self.clientsocket.sendall(display.encode('utf-8'))
                OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
                if OkCode == "clientHasntOpenedAFile":
                    print("Commande 'read <size>' annulée, le client n'a pas encore ouvert de fichier")
                elif OkCode != "000":
                    print("CODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                    break
                else:
                    self.readCommand()
            elif choix == '3':
                display = "Ok3"
                self.clientsocket.sendall(display.encode('utf-8'))
                OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
                if OkCode != "000":
                    print("CODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                    break
                self.closeCommand()
            elif choix == '4':
                display = "Ok4"
                self.clientsocket.sendall(display.encode('utf-8'))
                OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
                if OkCode != "000":
                    print("CODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                    break
                self.listCommand()
            elif choix == '5':
                display = "Ok5"
                self.clientsocket.sendall(display.encode('utf-8'))
                OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
                if OkCode != "000":
                    print("CODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                    break
                self.statCommand()
            elif choix == 'q':
                display = "Okq"
                self.clientsocket.sendall(display.encode('utf-8'))
                OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
                if OkCode != "000":
                    print("CODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                    break
            else:
                display = "CODE ERREUR Nr 001: "+ERROR_ARRAY['001']
                self.clientsocket.sendall(display.encode('utf-8'))
                OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
                if OkCode != "000":
                    print("CODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                    break

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
                print("CODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                return
        else:
            print("Ouverture du fichier: ", fileName, "...")
            # on sauvegarde le nom de fichier par thread client pour pouvoir le lire ensuite lors de l'exécution de la commande 'read' de celui-ci
            self.fileName = fileName
            self.fileOpenedId = open(VIDEO_PATH+fileName, 'rb')
            fileOpened = "Ok"
            self.clientsocket.sendall(fileOpened.encode('utf-8'))
            
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("CODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
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
                print("CODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                return
            #doit envoyer les N octets du fichier
            buffer = self.fileOpenedId.read(size-1)
            #pas besoin d'encode(), on transfert les octets en binaire
            self.clientsocket.sendall(buffer)
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("CODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                return
        else:
            print("\ttaille du fichier plus petit que <size> donné")
            #doit envoyer les N octets à lire
            NOctetsALire = os.path.getsize(VIDEO_PATH+self.fileName)
            self.clientsocket.sendall(str(NOctetsALire).encode('utf-8'))
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("CODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                return
            #doit envoyer les N octets du fichier
            buffer = self.fileOpenedId.read()
            self.clientsocket.sendall(buffer)
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("CODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                return

    def closeCommand(self):
        print("hello from closeCommand()")

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
            print("CODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
        
    def statCommand(self):
        print("hello from statCommand()")

    def run(self):
        print("Connexion de %s %s" % (self.ip, self.port, ))

        self.menu()

        # r = self.clientsocket.recv(2048)
        # print("%s"%r)
        # # envois de fichier
        # print("Ouverture du fichier: ", r, "...")
        # fp = open(r, 'rb')
        # self.clientsocket.send(fp.read())

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