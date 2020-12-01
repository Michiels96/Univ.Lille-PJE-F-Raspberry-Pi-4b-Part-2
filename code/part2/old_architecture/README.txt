PJE F Raspberry Pi 4b Part 2

Partie 1 (code/part1)
Patterns de commande pour exécuter les fichiers:
- server.py
    python3 server.py <PORT>
- openClient.py:
    python3 openClient.py <IP> <PORT> <filename>
- readClient.py:
    python3 readClient.py <IP> <PORT>
- closeClient.py:
    python3 closeClient.py <IP> <PORT>
- listClient:
    python3 listClient.py <IP> <PORT>
- statClient.py:
    python3 statClient.py <IP> <PORT> <filename>

Partie 2 (code/part2)
Patterns de commande pour exécuter les fichiers:
- master.py
    python3 master.py <PORT>
- publisher.py 
    Pour s'inscrire au master:
        python3 publisher.py <IpDuMaster> <PortDuMaster> <NomDuPublisher> <0>
    Pour alerter tous ses subscribers:
        python3 publisher.py <IpDuMaster> <PortDuMaster> <NomDuPublisher> <1>
- subscriber.py
    Pour s'inscrire au master:
        python3 subscriber.py <IpDuMaster> <PortDuMaster> <NomDuSubscriber> <NomDuPublisher> <0>
    Pour rester en écoute aux publishers auquel le subscriber est inscrit:
        python3 subscriber.py <PORT> <1>


    On a décidé que chaque subscriber, lorsqu'il est en mode serveur, que son port sera 8090.
    Il est sous-entendu qu'un subscriber ne peut s'inscrire et 
        écouter les publishers qui publient leur nouvelle video en même temps.
