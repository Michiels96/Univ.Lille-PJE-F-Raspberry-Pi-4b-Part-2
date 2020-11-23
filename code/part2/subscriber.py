# coding: utf-8

import socket
import sys
import os
import re
import threading




class Subscriber():

    def __init__(self, subscriberName, publisherToSubscribeTo):
        self.OkCode = "000"
        self.lock = threading.Lock()
        self.subscriberName = subscriberName
        self.publisherToSubscribeTo = publisherToSubscribeTo
        #self.command = command

    def main(self):
        #inscription au master
        # if self.command == '0':
        listOption = "inscrSubscriber"
        s.sendall(listOption.encode())

        readyForSendingPublisherName = (s.recv(1024)).decode('utf-8')
        if readyForSendingPublisherName != "okPublisherName":
            print("\tMaster n'est pas prêt à recevoir publisherName\n\n")
            return
        s.sendall(self.publisherToSubscribeTo.encode())

        
        
        readyForSendingSubscriberName = (s.recv(1024)).decode('utf-8')
        if readyForSendingSubscriberName != "okSubscriberName":
            print(readyForSendingSubscriberName, "\n\n")
            return
        s.sendall(self.subscriberName.encode())

        codeSubscriberSignedIn = (s.recv(1024)).decode('utf-8')
        if codeSubscriberSignedIn != "okSubscriberSignedIn":
            print(codeSubscriberSignedIn,"\n\n")
            s.sendall(self.OkCode.encode())
            return
        s.sendall(self.OkCode.encode())

        readyForRecievePublisherFileList = (s.recv(1024)).decode('utf-8')
        if readyForRecievePublisherFileList != "okPublisherFileList":
            print("\tErreur, le master n'est pas prêt à envoyer la liste des fichiers du publisher abonné.")
            s.sendall(self.OkCode.encode())
            return
        s.sendall(self.OkCode.encode())

        listeFichiers = (s.recv(1024)).decode('utf-8')
        s.sendall(self.OkCode.encode())
        print("Liste des fichiers du Publisher <", self.publisherToSubscribeTo,"> :")
        listeFichiers = re.search("'(.+)'", listeFichiers).group(1).split("', '")
        display = ''
        for i in listeFichiers:
            display += "\t"+i+"\n"
        print(display)
        print("\tsubscriber <", self.subscriberName,"> inscrit au Publisher <", self.publisherToSubscribeTo,"> !\n")

        self.lock.acquire()
        publisherArray[self.publisherToSubscribeTo] = listeFichiers
        print("ICII ", publisherArray)
        self.lock.release()
        

        # elif self.command == '1':
        #     while True:
        #         print( "En écoute...")

        # else:
        #     print("\tErreur, la commande n'est pas valide ou n'a pas été donné\n\n")

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
        print("publi ", publisherName)
        
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
        print("LABAS ", publisherArray)
        publisherArray[publisherName].append(newFileRecieved)
        print("Liste des fichiers du Publisher <", publisherName,"> :")
        print("\t", publisherArray[publisherName], "\n")
        self.lock.release()
        


    def run(self):
        print("Connexion de %s %s" % (self.ip, self.port, ))
        self.menu()
        print("publisher déconnecté...")



publisherArray = {}

#récupérer l'addr ip, le port et les arguments


if len(sys.argv) == 6 and sys.argv[5] == '0':
    ipMaster = sys.argv[1]
    portMaster = int(sys.argv[2])
    subscriberName = sys.argv[3]
    publisherToSubscribeTo = sys.argv[4]
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.connect(("127.0.0.1", 8080))
    s.connect((ipMaster, portMaster))
    newClient = Subscriber(subscriberName, publisherToSubscribeTo)
    newClient.main()

elif sys.argv[2] == '1':
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    port = int(sys.argv[1])
    tcpsock.bind(("",port))

    while True:
        print( "En écoute...")
        tcpsock.listen(10)
        (clientsocket, (ip, port)) = tcpsock.accept()
        newthread = SubscriberServer(ip, port, clientsocket)
        newthread.start()