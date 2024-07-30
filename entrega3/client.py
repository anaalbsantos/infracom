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
seq_number = 0
  

def make_pkt(seq_number, data):
    return str({'seq_number': seq_number, 'data': data}).encode()

def send(cmd, socket, addr):
    global seq_number
    while True:
        socket.settimeout(5)
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
            # socket.sendto(pkt, addr)
            print('timeout')
            pass

def handle_login(cmd, socket, addr):
    send(cmd, socket, addr)
    msg = receive(socket)

def receive(socket):
    global seq_number
    while True:
        socket.settimeout(5)
        
        try:
            msg, address = socket.recvfrom(1024)
            msg = eval(msg.decode())
            if msg is not None:
                
                if msg['seq_number'] == seq_number and msg['data'] != b'ACK':
                    print('msg received: ', msg['data'], 'and seq_number: ', msg['seq_number'])
                    pkt = make_pkt(seq_number, b'ACK')
                    socket.sendto(pkt, address)
                    seq_number = 1 - seq_number
                    return msg['data']
            else: 
                return
                
        except skt.timeout:
            continue

def rcv_msg(socket):
    while True:
        msg = receive(socket)
        if msg is not None:
            print(msg)

#threading.Thread(target=rcv_msg, args=(client_socket,), daemon=True).start()

try:
    while True:
        # # aqui ele deve receber o comando do usuário e enviar para o servidor em loop, mas receber as mensagens do servidor ao mesmo tempo        
        if client_socket.recv is not None:
            cmd = input()
            send(cmd, client_socket, server_addr)
            receive(client_socket)
        else:
            rcv_msg(client_socket)
except KeyboardInterrupt:
    print('Closing client')
    client_socket.close()