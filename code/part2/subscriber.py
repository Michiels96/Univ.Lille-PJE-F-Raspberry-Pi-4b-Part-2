# coding: utf-8

import socket
import sys
import os
import re
import threading
import json

publishersArray = {}

class SubscriberSignIn():

    def __init__(self, ipMaster, portMaster, subscriberName, publishersToSubscribeTo):
        self.OkCode = "000"
        self.lock = threading.Lock()
        self.ipMaster = ipMaster
        self.portMaster = portMaster
        self.subscriberName = subscriberName
        self.publishersToSubscribeTo = publishersToSubscribeTo

    def main(self):
        #inscription au master
        for publisherToSubscribeTo in publishersToSubscribeTo:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.ipMaster, self.portMaster))


            listOption = "inscrSubscriber"
            s.sendall(listOption.encode())

            readyForSendingPublisherName = (s.recv(1024)).decode('utf-8')
            if readyForSendingPublisherName != "okPublisherName":
                print("\tMaster n'est pas prêt à recevoir publisherName\n\n")
                return False
            s.sendall(publisherToSubscribeTo.encode())

            
            
            readyForSendingSubscriberName = (s.recv(1024)).decode('utf-8')
            if readyForSendingSubscriberName != "okSubscriberName":
                print(readyForSendingSubscriberName, "\n\n")
                return
            s.sendall(self.subscriberName.encode())

            codeSubscriberSignedIn = (s.recv(1024)).decode('utf-8')
            if codeSubscriberSignedIn != "okSubscriberSignedIn":
                print(codeSubscriberSignedIn,"\n\n")
                s.sendall(self.OkCode.encode())
                return False
            s.sendall(self.OkCode.encode())

            readyForRecievePublisherFileList = (s.recv(1024)).decode('utf-8')
            if readyForRecievePublisherFileList != "okPublisherFileList":
                print("\tErreur, le master n'est pas prêt à envoyer la liste des fichiers du publisher abonné.")
                s.sendall(self.OkCode.encode())
                return False
            s.sendall(self.OkCode.encode())

            listeFichiers = (s.recv(1024)).decode('utf-8')
            s.sendall(self.OkCode.encode())
            print("Liste des fichiers du Publisher <", publisherToSubscribeTo,"> :")
            listeFichiers = re.search("'(.+)'", listeFichiers).group(1).split("', '")
            display = ''
            for i in listeFichiers:
                display += "\t"+i+"\n"
            print(display)
            print("\tsubscriber <", self.subscriberName,"> inscrit au Publisher <", publisherToSubscribeTo,"> !\n")


            self.lock.acquire()
            publishersArray[publisherToSubscribeTo] = []
            publishersArray[publisherToSubscribeTo] = listeFichiers
            self.lock.release()

            s.close()
        return True


class SubscriberServer(threading.Thread):

    def __init__(self, ip, port, clientsocket):

        threading.Thread.__init__(self)
        self.OkCode = "000"
        self.lock = threading.Lock()
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port))

    def menu(self):

        #nom du publisher
        readyForRecievePublisherName = (self.clientsocket.recv(1024)).decode('utf-8')
        if readyForRecievePublisherName != 'okPublisherName':
            print("\tErreur, le publisher connecté n'est pas prêt à envoyer son nom")
            return 
        self.clientsocket.sendall(self.OkCode.encode())
        publisherName = (self.clientsocket.recv(1024)).decode('utf-8')

        publisherNameRecieved = "okPublisherNameRecieved"
        self.clientsocket.sendall(publisherNameRecieved.encode('utf-8'))


        #nom du nouveau fichier
        readyForRecieveNewFileName = (self.clientsocket.recv(1024)).decode('utf-8')
        if readyForRecieveNewFileName != 'okNewFileName':
            print("\tErreur, le publisher connecté n'est pas prêt à envoyer le nom du nouveau fichier")
            return 
        self.clientsocket.sendall(self.OkCode.encode())
        newFileName = (self.clientsocket.recv(1024)).decode('utf-8')
        newFileRecieved = "okNewFileNameRecieved"
        self.clientsocket.sendall(newFileRecieved.encode('utf-8'))


        self.lock.acquire()
        publishersArray[publisherName].append(newFileName)
        print("\tEcriture du nom du nouveau fichier dans la SD publishersArray")
        #saveDataIntoPublishersFile(True, publisherName, publishersArray[publisherName])
        print("\tFAIT!\n")
        print("liste des fichiers pour le publisher <", publisherName,">:")
        print(publishersArray[publisherName])
        self.lock.release()
    


    def run(self):
        print("Connexion de %s %s" % (self.ip, self.port))
        #récupérer les listes de fichiers des publishers auquel le subscriber est abonné
        self.lock.acquire()
        print("\tDEBUT DU PROGRAMME - LOAD SD publishersArray", publishersArray)
        self.lock.release()
        self.menu()
        print("publisher déconnecté...")
        print("\n\nEn écoute...")





ipMaster = sys.argv[1]
portMaster = int(sys.argv[2])
subscriberName = sys.argv[3]

#récupérer tous les publishers auquel le subscriber veut s'y abonner
publishersToSubscribeTo = []
for i in range(4, len(sys.argv)):
    publishersToSubscribeTo.append(sys.argv[i])

    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        tcpsock.bind(("",8090))
        tcpsock.close()
    except OSError:
        print("\n\tErreur, un subscriber tourne déjà sur cette machine\n")
        sys.exit()


#Phase 1: inscription du subscriber au master
newClient = SubscriberSignIn(ipMaster, portMaster, subscriberName, publishersToSubscribeTo)
continueCode = newClient.main()


if continueCode:
    #Phase 2: écoute de tous les publishers
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpsock.bind(("",8090))

    while True:
        print("Mode serveur\n\tEn écoute...")
        tcpsock.listen(10)
        (clientsocket, (ip, port)) = tcpsock.accept()
        newthread = SubscriberServer(ip, port, clientsocket)
        newthread.start()