#coding:utf-8
# Echo server program
import socket
import threading

def worker(conn, addr):
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data: break
            print("Received: ", data.decode('utf-8'))
            conn.sendall(data)
            
HOST =''            # Symbolic name meaning all available interfaces
PORT = 50007        # Arbitrary non-privileged port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    while True :
        conn, addr = s.accept() # accept a connection
        t1 = threading.Thread(target=worker, args=(conn, addr))
        t1.start()