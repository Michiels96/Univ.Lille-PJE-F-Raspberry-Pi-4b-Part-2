# coding: utf-8 

import socket
import threading
import time

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
            #obligé d'attendre une microseconde sinon la synchronisation ne peut se faire entre le serveur et le client
            time.sleep(0.01)
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

            if choix == '1':
                display = "choix 1"
                self.clientsocket.sendall(display.encode('utf-8'))
            elif choix == '2':
                display = "choix 2"
                self.clientsocket.sendall(display.encode('utf-8'))
            elif choix == '3':
                display = "choix 3"
                self.clientsocket.sendall(display.encode('utf-8'))
            elif choix == '4':
                display = "choix 4"
                self.clientsocket.sendall(display.encode('utf-8'))
            elif choix == '5':
                display = "choix 5"
                self.clientsocket.sendall(display.encode('utf-8'))
            elif choix == 'q':
                display = "choix Q"
                self.clientsocket.sendall(display.encode('utf-8'))
            else:
                display = "pas compris, recommencez!"
                self.clientsocket.sendall(display.encode('utf-8'))

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