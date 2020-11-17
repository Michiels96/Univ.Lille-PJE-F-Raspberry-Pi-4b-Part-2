# coding: utf-8

import socket
import sys
import os


class Subscriber():

    def __init__(self, subscriberName, publisherToSubscribeTo, command):
        self.OkCode = "000"
        self.subscriberName = subscriberName
        self.publisherToSubscribeTo = publisherToSubscribeTo
        self.command = command

    def main(self):
        #inscription au master
        if self.command == '0':
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
            print(listeFichiers)
            print("\tsubscriber <", self.subscriberName,"> inscrit au Publisher <", self.publisherToSubscribeTo,"> !\n")

        elif self.command == '1':
            abc = 'abc'
        else:
            print("\tErreur, la commande n'est pas valide ou n'a pas été donné\n\n")



#récupérer l'addr ip, le port et les arguments
ipMaster = sys.argv[1]
portMaster = int(sys.argv[2])

if len(sys.argv) == 6:
    subscriberName = sys.argv[3]
    publisherToSubscribeTo = sys.argv[4]
    command = sys.argv[5]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.connect(("127.0.0.1", 8080))
    s.connect((ipMaster, portMaster))
    newClient = Subscriber(subscriberName, publisherToSubscribeTo, command)
    newClient.main()
else:
    subscriberName = 'null'
    publisherToSubscribeTo = 'null'
    command = sys.argv[3]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.connect(("127.0.0.1", 8080))
    s.connect((ipMaster, portMaster))
    newClient = Subscriber(subscriberName, publisherToSubscribeTo, command)
    newClient.main()