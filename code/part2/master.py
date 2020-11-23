# coding: utf-8 

import socket
import threading
import sys
import copy

# VARIABLES GLOBALES
ERROR_ARRAY = {
    '001': 'Le publisher n\'a pas confirmé la réception du paquet venant du Master!',
    '002': 'Le subscriber n\'a pas confirmé la réception du paquet venant du Master!',
    '003': 'Le nom du publisher est déjà inscrit au Master',
    '004': 'Le publisher connecté n\'est pas inscrit au Master',
    '005': 'Le subscriber est déjà inscrit au publisher donné'
}

publisherSubscriberArray = {}

class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):

        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port, ))

    def menu(self):  
        #inscriptions pour un publisher et un subscriber
        choix = (self.clientsocket.recv(1024)).decode('utf-8')
        print("RECU du publisher/subscriber --> ", choix)

        #Partie publisher
        if choix == 'inscrPublisher':
            #reception de l'id du publisher connecté
            readyForRecievePublisherName = "okPublisherName"
            self.clientsocket.sendall(readyForRecievePublisherName.encode('utf-8'))
            publisherName = (self.clientsocket.recv(1024)).decode('utf-8')
            
            #vérification si le publisher n'est pas déjà inscrit
            self.lock.acquire()
            estInscrit = self.checkIfPublisherIsSignedIn(publisherName)
            self.lock.release()
            if estInscrit == True:
                display = "\tCODE ERREUR Nr 003: "+ERROR_ARRAY['003']
                print(display)
                return
            display = "nouvPublisher"
            self.clientsocket.sendall(display.encode('utf-8'))
            #reception de la liste des fichiers déjà existants pour le publisher à inscrire
            listeFichiers = (self.clientsocket.recv(1024)).decode('utf-8')
            listeFichiers = listeFichiers.split("\n")
            #enlever le dernier \n
            listeFichiers.pop()
            self.lock.acquire()
            publisherSubscriberArray[publisherName] = {}
            publisherSubscriberArray[publisherName]["fileList"] = listeFichiers
            publisherSubscriberArray[publisherName]["subscribers"] = {}
            # publisherSubscriberArray[publisherName]["subscribers"]["sub1"] = "127.0.45.89"
            # publisherSubscriberArray[publisherName]["subscribers"]["sub2"] = "192.168.1.2"
            self.lock.release()

            receptionCode = "inscriptionOk"
            self.clientsocket.sendall(receptionCode.encode('utf-8'))

            self.lock.acquire()
            #print("\t", publisherSubscriberArray)
            print("\tLEN - nombre de fichiers du publisher <", publisherName,">", len(publisherSubscriberArray[publisherName]["fileList"]))
            self.lock.release()

        elif choix == 'getSubscribers':
            #reception de l'id du publisher connecté
            readyForRecievePublisherName = "okPublisherName"
            self.clientsocket.sendall(readyForRecievePublisherName.encode('utf-8'))
            publisherName = (self.clientsocket.recv(1024)).decode('utf-8')

            readyForRecieveNewFileName = "okNewFileName"
            self.clientsocket.sendall(readyForRecieveNewFileName.encode('utf-8'))
            newFileName = (self.clientsocket.recv(1024)).decode('utf-8')

            #vérification si le publisher est déjà inscrit
            self.lock.acquire()
            estInscrit = self.checkIfPublisherIsSignedIn(publisherName)
            self.lock.release()
            if estInscrit == False:
                codePublisherName = "\tCODE ERREUR Nr 004: "+ERROR_ARRAY['004']
                print(codePublisherName)
                self.clientsocket.sendall(codePublisherName.encode('utf-8'))
                OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
                if OkCode != "000":
                    print("\tCODE ERREUR Nr 001: "+ERROR_ARRAY['001'])
                    return
            else:
                codePublisherInscrit = "okPublisherInscrit"
                self.clientsocket.sendall(codePublisherInscrit.encode('utf-8'))
                # OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
                # if OkCode != "000":
                #     print("\tCODE ERREUR Nr 001: "+ERROR_ARRAY['001'])
                #     return

                #ajouter le nom du nouveau fichier dans la liste des fichiers du publisher inscrit
                #ceci permet aux nouveaux subscribers de recevoir la liste des fichiers du publisher, auxquels ils s'abonnent, à jour
                self.lock.acquire()
                publisherSubscriberArray[publisherName]["fileList"].append(newFileName)
                print("\tLEN - nombre de fichiers du publisher <", publisherName,">", len(publisherSubscriberArray[publisherName]["fileList"]))
                self.lock.release()
                

                #renvoyer la liste de ses subscribers
                readyToSendSubscribers = (self.clientsocket.recv(1024)).decode('utf-8')
                if readyToSendSubscribers == "okSubscribers":
                    self.lock.acquire()
                    subscribers = copy.copy(publisherSubscriberArray[publisherName]["subscribers"])
                    self.lock.release()
                    self.clientsocket.sendall(str(subscribers).encode('utf-8'))
                    OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
                    if OkCode != "000":
                        print("\tCODE ERREUR Nr 001: "+ERROR_ARRAY['001'])
                        return
                else:
                    print("\tError: confirmation de reception des subscribers non-reçue\n\n")
                
                    
        #Partie subscriber
        elif choix == 'inscrSubscriber':
            #reception de l'id du publisher connecté
            readyForRecievePublisherName = "okPublisherName"
            self.clientsocket.sendall(readyForRecievePublisherName.encode('utf-8'))
            publisherName = (self.clientsocket.recv(1024)).decode('utf-8')
            
            #vérification si le publisher n'est pas déjà inscrit
            self.lock.acquire()
            estInscrit = self.checkIfPublisherIsSignedIn(publisherName)
            self.lock.release()
            if estInscrit == False:
                codeNoPublisher = "\tCODE ERREUR Nr 004: "+ERROR_ARRAY['004']
                print(codeNoPublisher)
                self.clientsocket.sendall(codeNoPublisher.encode('utf-8'))
                return

            #reception de l'id du subscriber connecté
            readyForRecieveSubscriberName = "okSubscriberName"
            self.clientsocket.sendall(readyForRecieveSubscriberName.encode('utf-8'))
            subscriberName = (self.clientsocket.recv(1024)).decode('utf-8')

            #vérification si le subscriber n'est pas déjà inscrit dans la liste des subscribers du publisher donné
            self.lock.acquire()
            estInscrit = self.checkIfSubscriberIsInPublisherSubscribers(subscriberName, publisherName)
            self.lock.release()
            if estInscrit == True:
                codeSubscriberSignedIn = "\tCODE ERREUR Nr 005: "+ERROR_ARRAY['005']
                print(codeSubscriberSignedIn)
                self.clientsocket.sendall(codeSubscriberSignedIn.encode('utf-8'))
                OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
                if OkCode != "000":
                    print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                return


            codeSubscriberSignedIn = "okSubscriberSignedIn"
            self.clientsocket.sendall(codeSubscriberSignedIn.encode('utf-8'))
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                return

            #envois de la liste des fichiers du publisher abonné
            readyForRecievePublisherFileList = "okPublisherFileList"
            self.clientsocket.sendall(readyForRecievePublisherFileList.encode('utf-8'))
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                return
            
            self.lock.acquire()
            listeFichiers = copy.copy(publisherSubscriberArray[publisherName]["fileList"])
            self.lock.release()
            self.clientsocket.sendall(str(listeFichiers).encode('utf-8'))
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("\tCODE ERREUR Nr 002: "+ERROR_ARRAY['002'])
                return

            self.lock.acquire()
            print("\t(", len(publisherSubscriberArray[publisherName]["subscribers"]),") subscribers de <", publisherName, "> -> ", publisherSubscriberArray[publisherName]["subscribers"])
            self.lock.release()

        # elif choix == 'newFile':
        #     abc = 'abc'







    def checkIfPublisherIsSignedIn(self, publisherName):
        if publisherName in publisherSubscriberArray:
            return True
        else:
            return False

    def checkIfSubscriberIsInPublisherSubscribers(self, subscriberName, publisherName):
        if subscriberName in publisherSubscriberArray[publisherName]["subscribers"]:
            return True
        else:
            #au lieu de re-bloquer une 2eme fois le mutex, on l'inscrit aussi ici
            publisherSubscriberArray[publisherName]["subscribers"][subscriberName] = str(self.ip)
            return False

    def run(self):
        print("Connexion de %s %s" % (self.ip, self.port, ))
        self.menu()
        print("publisher/subscriber déconnecté...")



tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# "" pour l'HOST permet de recevoir une connexion de n'importe quelle addr IP
port = int(sys.argv[1])
tcpsock.bind(("",port))


while True:
    print( "En écoute...")
    tcpsock.listen(10)
    (clientsocket, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()