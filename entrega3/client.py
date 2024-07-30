import socket as skt    # Importando as bibliotecas
import random
import threading
import time

# Setando as informações do socket
server_name = 'localhost'
server_port = 12000
client_port = 0 # define 0 para que o SO escolha uma porta disponível
server_addr = (server_name, server_port)  # Definindo a tupla que contem o IP e a Porta do servidor
client_addr = (server_name, client_port)  # Definindo a tupla que contem o IP e a Porta do cliente

client_socket = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)  # Criando socket do cliente para UDP
client_socket.bind(client_addr)

new_msg = ""
seq_number = 0
lock = threading.Lock()
  

def make_pkt(seq_number, data):
    return str({'seq_number': seq_number, 'data': data}).encode()

def send(cmd, socket, addr):
    global seq_number
    while True:
        socket.settimeout(3)
        pkt = make_pkt(seq_number, cmd)

        if random.random() > 0.1:
            socket.sendto(pkt, addr)
            print('sending')

        try:
            msg, address = socket.recvfrom(1024)
            msg = eval(msg.decode())

            while msg is None:      
                msg, address = socket.recvfrom(1024)
                msg = eval(msg.decode())  

            if msg['data'] == b'ACK' and msg['seq_number'] == seq_number:
                seq_number = 1 - seq_number
                print('ACK received')
                break
        except skt.timeout:
            print('timeout')
            pass

def receive(socket):
    global seq_number
    socket.settimeout(3)
    while True:        
        try:
            # print('oi')
            msg, address = socket.recvfrom(1024)
            msg = eval(msg.decode())

            if msg is not None:
                if msg['seq_number'] == seq_number and msg['data'] != b'ACK':
                    print('msg received: ', msg['data'], 'and seq_number: ', msg['seq_number'])
                    pkt = make_pkt(seq_number, b'ACK')
                    socket.sendto(pkt, address)
                    seq_number = 1 - seq_number
                elif  msg['seq_number'] != seq_number:
                    print('quero seq ', seq_number, 'mas recebi ', msg['seq_number'])
                    pkt = make_pkt(1 - seq_number, b'ACK')
                    socket.sendto(pkt, address)

        except skt.timeout:
            continue

def rcv_msg(socket):
    while True:
        msg = receive(socket)
        if msg is not None:
            print(msg)


def handle_input():
    while True:
        cmd = input()
        send(cmd, client_socket, server_addr)



try:
    th_input = threading.Thread(target=handle_input)
    th_rcv = threading.Thread(target=receive, args=(client_socket,))
    th_input.start()
    th_rcv.start()
    th_input.join()
    th_rcv.join()

except KeyboardInterrupt:
    print('Closing client')
    client_socket.close()