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
    Pour s'inscrire au master et être ensuite à l'écoute des publishers connectés:
        python3 subscriber.py <IpDuMaster> <PortDuMaster> <NomDuSubscriber> <NomDuPublisher1> <NomDuPublisher2> <NomDuPublisher3> etc.

    On a décidé que chaque subscriber, lorsqu'il est en mode serveur, que son port sera 8090.

    Il est sous-entendu qu'un seul subscriber ne peut s'exécuter que sur une machine à la fois
    car le port 8090 ne peut être utilisé que par 1 subscriber à la fois.
