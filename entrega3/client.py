import socket as skt    # Importando as bibliotecas
import random
import threading
import time
from rdt3 import *

def try_recv_msg(client):
    while True:
        if not client.connected:
            # print("matando thread")
            break
        if client.has_message():
            try:
                msg, address = client.receive()
                print(msg)
            except:
                pass

def get_user():
    while True:
        msg = input('type something: ')
        
        if len(msg) < 7:
            continue 
        
        cmd = msg[:6]
        if cmd == 'login ':
            return msg

client = connection()
th_recv_msg = threading.Thread(target=try_recv_msg, args=(client,))

try:
    client.open_socket('localhost', 12000, 'client')

    user = get_user()
    client.send(user.encode())
    th_recv_msg.start()

    while True:
        cmd = input('-')

        if cmd is not None:
            # print(cmd)
            client.send(cmd.encode())

            if cmd == 'logout':
                break
    
    client.close_connection()
    th_recv_msg.join()
    print('cabou')

except KeyboardInterrupt:
    client.close_connection()
    th_recv_msg.join()
    print('cabou')