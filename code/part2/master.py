# coding: utf-8 

import socket
import threading
import copy

# VARIABLES GLOBALES
ERROR_ARRAY = {
    '001': 'Le publisher n\'a pas confirmé la réception du paquet venant du Master!',
    '002': 'Le subscriber n\'a pas confirmé la réception du paquet venant du Master!',
    '003': 'Le publisher connecté à déjà été inscrit au Master',
    '004': 'Le publisher connecté n\'est pas inscrit au Master'
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
            else:
                publisherSubscriberArray[publisherName] = []
                display = "inscriptionOk"
                
            self.clientsocket.sendall(display.encode('utf-8'))
            OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
            if OkCode != "000":
                print("\tCODE ERREUR Nr 001: "+ERROR_ARRAY['001'])

        elif choix == 'getSubscribers':
            #reception de l'id du publisher connecté
            readyForRecievePublisherName = "okPublisherName"
            self.clientsocket.sendall(readyForRecievePublisherName.encode('utf-8'))
            publisherName = (self.clientsocket.recv(1024)).decode('utf-8')

            #vérification si le publisher est déjà inscrit
            self.lock.acquire()
            estInscrit = self.checkIfPublisherIsSignedIn(publisherName)
            self.lock.release()
            if estInscrit == False:
                display = "\tCODE ERREUR Nr 004: "+ERROR_ARRAY['004']
                print(display)
                self.clientsocket.sendall(display.encode('utf-8'))
                OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
                if OkCode != "000":
                    print("\tCODE ERREUR Nr 001: "+ERROR_ARRAY['001'])
                    return
            else:
                #renvoyer la liste de ses subscribers
                self.lock.acquire()
                subscribers = copy.deepcopy(publisherSubscriberArray[publisherName])
                self.lock.release()
                self.clientsocket.sendall(subscribers.encode('utf-8'))
                OkCode = (self.clientsocket.recv(1024)).decode('utf-8')
                if OkCode != "000":
                    print("\tCODE ERREUR Nr 001: "+ERROR_ARRAY['001'])
                    return
                    
            #Partie subscriber


    def checkIfPublisherIsSignedIn(self, publisherName):
        if publisherName in publisherSubscriberArray:
            return True
        else:
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
    tcpsock.listen(10)
    print( "En écoute...")
    (clientsocket, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()