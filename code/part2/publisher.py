# coding: utf-8

import socket
import sys
import os

# path à utiliser pour le raspberry pi 
#VIDEO_PATH = "/media/usb0/record/"
VIDEO_PATH = "/root/record_sample/"

class Publisher():

    def __init__(self, publisherName, command):
        ## cette variable transmet la valeur '000' au serveur pour lui indiquer que le client a bien reçu ce que le serveur lui a envoyé, 
        ## ceci permet d'avoir une architecture synchrone 
        self.OkCode = "000"
        self.publisherName = publisherName
        self.command = command

    def main(self):
        #Inscription au master
        if self.command == '0':
            listOption = "inscrPublisher"
            s.sendall(listOption.encode())
            readyForSendingPublisherName = (s.recv(1024)).decode('utf-8')
            if readyForSendingPublisherName != "okPublisherName":
                print("\tMaster n'est pas prêt à recevoir publisherName\n")
            else:
                s.sendall(self.publisherName.encode())
                receptionCode = (s.recv(1024)).decode('utf-8')

                if receptionCode == "nouvPublisher":
                    videoListDisplay = ""
                    for f in os.listdir(VIDEO_PATH):
                        if not f.startswith('.'):
                            videoListDisplay += (f+"\n")
                    s.sendall(videoListDisplay.encode())

                    receptionCode = (s.recv(1024)).decode('utf-8')
                    if receptionCode == "inscriptionOk":
                        print("\tPublisher <", self.publisherName,"> inscrit!\n\n")
                else:
                    print(receptionCode, "\n")
        
        #vérification en continu du dossier record_sample 
        #pour aller alerter les subscribers en cas d'un ajout de fichier dans le dossier record_sample
        elif self.command == '1':
            videoList = []
            for f in os.listdir(VIDEO_PATH):
                if not f.startswith('.'):

                    videoList.append(f)
            alreadyDisplayedWithoutAddingAFile = False
            while True:
                if alreadyDisplayedWithoutAddingAFile == False:
                    print("\n\tEn cours d'analyse de nouveaux fichiers ...\n")
                    alreadyDisplayedWithoutAddingAFile = True
                
                for f in os.listdir(VIDEO_PATH):
                    if not f.startswith('.') and f not in videoList:
                        print("\n\tNouvelle video/fichier! <", f,">\n")
                        alreadyDisplayedWithoutAddingAFile = False
                        videoList.append(f)
                        #reception de tous les noms et addr ip de ses subscribers de la part du master
                        listOption = "getSubscribers"
                        s.sendall(listOption.encode())

                        readyForSendingPublisherName = (s.recv(1024)).decode('utf-8')
                        if readyForSendingPublisherName != "okPublisherName":
                            print("\tMaster n'est pas prêt à recevoir publisherName\n")
                            s.sendall(self.OkCode.encode())
                            return
                        s.sendall(self.publisherName.encode())

                        readyForSendingNewFileName = (s.recv(1024)).decode('utf-8')
                        if readyForSendingNewFileName != "okNewFileName":
                            print("\tMaster n'est pas prêt à recevoir le nom du nouveau fichier\n")
                            s.sendall(self.OkCode.encode())
                            return
                        s.sendall(str(f).encode())

                        codePublisherInscrit = (s.recv(1024)).decode('utf-8')
                        if codePublisherInscrit != "okPublisherInscrit":
                            print(codePublisherInscrit, "\n\n")
                            s.sendall(self.OkCode.encode())
                            return 


                        #reception des subscribers
                        readyForRecievingSubscribers = "okSubscribers"
                        s.sendall(readyForRecievingSubscribers.encode())

                        print("\tReception des subscribers ...")
                        subscribers = (s.recv(1024)).decode('utf-8')

                        print("\tSubscribers:\n\t\t", subscribers)
                        subscribers = eval(subscribers)

                        s.sendall(self.OkCode.encode()) 

                        #envoyer le nom du nouveau fichier a chaque subscriber
                
        else:
            print("\tErreur, le dernier argument n'est pas valide ou n'a pas été donné\n\n")




#récupérer l'addr ip, le port et les arguments
ipMaster = sys.argv[1]
portMaster = int(sys.argv[2])
publisherName = sys.argv[3]
command = sys.argv[4]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect(("127.0.0.1", 8080))
s.connect((ipMaster, portMaster))

newClient = Publisher(publisherName, command)
newClient.main()