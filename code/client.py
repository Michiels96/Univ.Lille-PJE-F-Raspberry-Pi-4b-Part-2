# coding: utf-8

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 8080))

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
    print("Recu -->", paquet.decode(), "\n")
    


# print("Le nom du fichier que vous voulez récupérer:")
# file_name = input(">> ") # utilisez raw_input() pour les anciennes versions python
# s.send(file_name.encode())
# file_name = 'data/%s' % (file_name,)

# #reception de fichier
# r = s.recv(9999999)
# with open(file_name,'wb') as _file:
#     _file.write(r)
# print("Le fichier a été correctement copié dans : %s." % file_name)