import socket as skt    #importando as bibliotecas
import os
from time import sleep
import math
from rdt3 import *

#Setando as informações do socket
ip = 'localhost' # IP do sevidor
server_port = 12000
server_socket = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)
server_addr = (ip, server_port)
server_socket.bind(server_addr) 
print('server is ready to receive')

# lista de clientes conectados
users = {}

# Numero de sequencia para rdt3.0
seq_number = 0



try:
    while True:
        cmd, seq_number, client_addr = rdt_rcv(server_socket, seq_number)
        cmd = cmd.decode()

        if cmd.startswith("login"):
            user = cmd.split(' ')[1]
            users[user] = client_addr
            udt_send(server_socket, seq_number, f'você está online!', client_addr)
            continue
    
except KeyboardInterrupt:
    server_socket.close()
    exit()
