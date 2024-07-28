import socket as skt    # Importando as bibliotecas
import random
import threading

# Setando as informações do socket
server_name = 'localhost'
server_port = 12000
client_port = 0 # define 0 para que o SO escolha uma porta disponível
server_addr = (server_name, server_port)  # Definindo a tupla que contem o IP e a Porta do servidor
client_addr = (server_name, client_port)  # Definindo a tupla que contem o IP e a Porta do cliente

client_socket = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)  # Criando socket do cliente para UDP
client_socket.bind(client_addr)

new_msg = ""

def send(cmd):
    while True:
        client_socket.settimeout(5)

        if random.random() > 0.1:
            client_socket.sendto(cmd.encode(), server_addr)
            print('sending')
        try:
            msg, address = client_socket.recvfrom(1024)

            if msg == b'ACK':
                print('ACK received')
                break
        except skt.timeout:
            client_socket.sendto(cmd.encode(), server_addr)
            print('resending')
            pass


def receive():
    while True:
        client_socket.settimeout(5)
        
        try:
            msg, address = client_socket.recvfrom(1024)
            # msg = msg.decode()

            if msg != b'ACK':
                print('msg received: ', msg.decode())
                client_socket.sendto(b'ACK', address)
                break
                
        except skt.timeout:
            continue

threading.Thread(target=receive).start()

while True:
    cmd = input()
    send(cmd)