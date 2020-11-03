# coding: utf-8 

import socket
import threading

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
            print("1) 'open <filename>' pour ouvrir un fichier passé en paramètre en lecture")
            print("2) 'read <size>' pour lire le fichier ouvert précédemment \n\t(Uniquement si un fichier a été ouvert précédemment)")
            print("3) 'close' pour fermer un fichier \n\t(Uniquement si un fichier a été ouvert précédemment)")
            print("4) 'list' pour afficher l'arborescence des fichiers")
            print("5) 'stat <filename>' pour afficher les propriétés du fichier passé en paramètre")
            print("'q' pour se déconnecter")
            try:
                choix = input()
            except:
                print("Erreur, saisie incorrecte!")
                continue

            if choix == '1':
                print("choix 1")
            elif choix == '2':
                print("choix 2")
            elif choix == '3':
                    print("choix 3")
            elif choix == '4':
                print("choix 4")
            elif choix == '5':
                print("choix 5")
            elif choix == 'q':
                print("choix q")
            else:
                print("pas compris, recommencez!")

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