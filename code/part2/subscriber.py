# coding: utf-8

import socket
import sys
import os
import re
import threading

class Subscriber():

    def __init__(self, subscriberName, publisherToSubscribeTo):
        self.OkCode = "000"
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

        # elif self.command == '1':
        #     while True:
        #         print( "En écoute...")

        else:
            print("\tErreur, la commande n'est pas valide ou n'a pas été donné\n\n")

class SubscriberServer(threading.Thread):

    def __init__(self, ip, port, clientsocket):

        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port, ))

    def menu():


    def run(self):
        print("Connexion de %s %s" % (self.ip, self.port, ))
        self.menu()
        print("publisher déconnecté...")

#récupérer l'addr ip, le port et les arguments


if len(sys.argv) == 6:
    ipMaster = sys.argv[1]
    portMaster = int(sys.argv[2])
    subscriberName = sys.argv[3]
    publisherToSubscribeTo = sys.argv[4]
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.connect(("127.0.0.1", 8080))
    s.connect((ipMaster, portMaster))
    newClient = Subscriber(subscriberName, publisherToSubscribeTo, command)
    newClient.main()
else:
    # subscriberName = 'null'
    # publisherToSubscribeTo = 'null'
    # command = sys.argv[3]
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # #s.connect(("127.0.0.1", 8080))
    # s.connect((ipMaster, portMaster))

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