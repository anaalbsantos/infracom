import socket as skt    # Importando as bibliotecas
import os
import math
from rdt3 import *
import threading

# Setando as informações do socket
server_name = 'localhost'
server_port = 12000
client_port = 12001
server_addr = (server_name, server_port)  # Definindo a tupla que contem o IP e a Porta do servidor
client_addr = (server_name, client_port)  # Definindo a tupla que contem o IP e a Porta do cliente

client_socket = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)  # Criando socket do cliente para UDP
client_socket.bind(client_addr)

seq_number = 0

# Definindo o recebimento dos pacotes
def receive_msg():
    global seq_number

    while True:
        data, seq_number, addr = rdt_rcv(client_socket, seq_number)
        if data != b'ACK':
            print(data)

threading.Thread(target=receive_msg).start()

try:
    while True:
        cmd = input()                                                                                # Recebe o comando do usuário
        seq_number = udt_send(client_socket, seq_number, cmd.encode(), server_addr)                  # Envia o comando para o servidor
except KeyboardInterrupt:
    client_socket.close()
    exit()