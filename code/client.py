# coding: utf-8

import socket


## cette variable transmet la valeur '000' au serveur pour lui indiquer que le client a bien reçu ce que le serveur lui a envoyé, 
## ceci permet d'avoir une architecture synchrone 
OkCode = "000"
#booléen pour savoir si un fichier a déjà été ouvert par le client
fileAlreadyOpen = False
fileNameSaved = ''
# path à utiliser pour le raspberry pi 
#VIDEO_PATH = "/media/usb0/record/"
VIDEO_PATH = "/root/record_sample/"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 8080))

def openCommandResponse():
    readyForSendingFilename = (s.recv(1024)).decode('utf-8')
    if readyForSendingFilename != "OkFilename":
        print("Serveur n'est pas prêt à recevoir filename")
        return
    fileName = ''
    while True:
        try:
            print("Introduisez le nom du fichier à ouvrir: ")
            fileName = input()
            if fileName == '':
                raise ValueError
            else:
                break
        except:
            print("\tErreur, saisie incorrecte! recommencez")
            continue

    s.sendall(fileName.encode())
    fileExists = (s.recv(1024)).decode('utf-8')
    if fileExists == "noFile":
        print("\tErreur, le fichier n'existe pas ou n'est pas lisible\n\n")
        s.sendall(OkCode.encode())
    else:
        global fileAlreadyOpen
        fileAlreadyOpen = True
        global fileNameSaved
        fileNameSaved = fileName
        print("\tFichier '",fileName,"' ouvert!\n")
        s.sendall(OkCode.encode())

def readCommandResponse():
    readyForSendingSize = (s.recv(1024)).decode('utf-8')
    if readyForSendingSize != "OkSize":
        print("Serveur n'est pas prêt à recevoir <size>")
        return
    size = 0
    while True:
        try:
            print("Introduisez <size>:")
            size = input()
            size = int(size)
            if size == '':
                raise ValueError
            elif size < 1:
                print("Erreur, <size> trop petit")
            else:
                break
        except:
            print("\tErreur, saisie incorrecte! recommencez")
            continue

    s.sendall(str(size).encode())
    #reçoit les N octets du fichier à lire
    NOctetsALire = int((s.recv(1024)).decode('utf-8'))
    s.sendall(OkCode.encode())
    buffer = s.recv(NOctetsALire)
    #ecrit les octets dans un fichier
    with open(VIDEO_PATH+"copy-"+fileNameSaved, 'wb') as fileOpenedId:
        fileOpenedId.write(buffer)
    s.sendall(OkCode.encode())
    print("\tFichier '", fileNameSaved,"' lu!\n\n")

def closeCommandResponse():
    return

def listCommandResponse():
    print("Liste de tous les fichiers dans le répertoire:")
    display = (s.recv(1024)).decode('utf-8')
    print(display)
    s.sendall(OkCode.encode())

def statCommandResponse():
    return




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
    #print("Recu -->", serverResponse, "\n")

    if serverResponse == "Ok1":
        if fileAlreadyOpen == True:
            print("\tErreur, vous avez déjà ouvert un fichier\n")
            fileAlreadyOpened = "clientAlreadyOpenedAnotherFile"
            s.sendall(fileAlreadyOpened.encode())
        else:
            s.sendall(OkCode.encode())
            openCommandResponse()
    elif serverResponse == "Ok2":
        if fileAlreadyOpen == False:
            print("\tErreur, vous n'avez pas encore ouvert de fichier\n")
            fileAlreadyOpened = "clientHasntOpenedAFile"
            s.sendall(fileAlreadyOpened.encode())
        else:
            s.sendall(OkCode.encode())
            readCommandResponse()
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