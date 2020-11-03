# coding: utf-8

import socket


## cette variable transmet la valeur '000' au serveur pour lui indiquer que le client a bien reçu ce que le serveur lui a envoyé, 
## ceci permet d'avoir une architecture synchrone 
OkCode = "000"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 8080))

def openCommandResponse():
    print("Im in openCommandResponse()")

def readCommandResponse():
    abc = ''

def closeCommandResponse():
    abc = ''

def listCommandResponse():
    print("Liste de tous les fichiers dans le répertoire:")
    display = (s.recv(1024)).decode('utf-8')
    print(display)
    s.sendall(OkCode.encode())

def statCommandResponse():
    abc = ''




#reception du menu
choix = ''
while choix != "q":
    
    menu = s.recv(1024)
    print(menu.decode())

    while True:
        try:
            print("choisissez: ")
            choix = input()
            if choix == '':
                raise ValueError
            else:
                break
        except:
            print("Erreur, saisie incorrecte!")
            continue
            
    #envois de la reponse
    s.sendall(choix.encode())
    #reception de l'action demandée
    paquet = s.recv(1024)
    serverResponse = paquet.decode()
    print("Recu -->", serverResponse, "\n")

    if serverResponse == "Ok1":
        s.sendall(OkCode.encode())
        openCommandResponse()
    elif serverResponse == "Ok2":
        s.sendall(OkCode.encode())
    elif serverResponse == "Ok3":
        s.sendall(OkCode.encode())
    elif serverResponse == "Ok4":
        s.sendall(OkCode.encode())
        listCommandResponse()
    elif serverResponse == "Ok5":
        s.sendall(OkCode.encode())
    elif serverResponse == "Okq":
        s.sendall(OkCode.encode())
        break
    else:
        #erreur reçue du serveur
        print(serverResponse)
        s.sendall(OkCode.encode())
    


# print("Le nom du fichier que vous voulez récupérer:")
# file_name = input(">> ") # utilisez raw_input() pour les anciennes versions python
# s.send(file_name.encode())
# file_name = 'data/%s' % (file_name,)

# #reception de fichier
# r = s.recv(9999999)
# with open(file_name,'wb') as _file:
#     _file.write(r)
# print("Le fichier a été correctement copié dans : %s." % file_name)