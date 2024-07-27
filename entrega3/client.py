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
            try:
                msg, address = client_socket.recvfrom(1024)

                if msg.decode() == 'ACK':
                    break
            except skt.timeout:
                client_socket.sendto(cmd.encode(), server_addr)
                pass
        # else:
        #     if server_addr != address:
        #         continue
        #     ack = define_ack(cmd, msg)

def receive():
    global new_msg
    while True:
        client_socket.settimeout(5)
        
        try:
            msg, address = client_socket.recvfrom(1024)
            msg = msg.decode()

            if msg == 'ACK':
                client_socket.sendto(b'ACK', server_addr)
                break
                
            if msg != new_msg and msg is not None:
                new_msg = msg
                print(msg)
        except skt.timeout:
            pass

threading.Thread(target=receive).start()

while True:
    cmd = input()
    send(cmd)