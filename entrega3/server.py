import socket as skt    #importando as bibliotecas
import random

#Setando as informações do socket
ip = 'localhost' # IP do sevidor
server_port = 12000
server_socket = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)
server_addr = (ip, server_port)
server_socket.bind(server_addr) 
print('server is ready to receive')

# lista de clientes conectados
users = {}
new_msg = ""

def receive():
    # global new_msg
    while True:
        server_socket.settimeout(5)
        
        try:
            msg, address = server_socket.recvfrom(1024)
            msg = msg.decode()

            if msg:
                print('msg received: ', msg)
                server_socket.sendto(b'ACK', address)
                return msg, address
                
        except skt.timeout:
            continue

        
def send(cmd, socket, addr):

    while True:
        socket.settimeout(5)

        if random.random() > 0.1:
            socket.sendto(cmd.encode(), addr)
            print('sending')
        try:
            msg, address = socket.recvfrom(1024)

            if address != addr:
                continue
            if msg == b'ACK':
                print('ACK received')
                break
        except skt.timeout:
            socket.sendto(cmd.encode(), addr)
            pass
    
def handle_msg(msg, client_addr):
    global users

    if msg.startswith('login'):
        if client_addr in users.values():
            response = 'você já está logado'
        else:
            name = msg.split(' ')[1]
            users[name] = client_addr
            print(f'{name} connected')
            response = f'você está online!'
    elif msg.startswith('list'):
        response = 'Usuários online:\n'
        for user in users:
            response += f'{user}\n'
    else:
        response = 'comando inválido'
    
    send(response, server_socket, client_addr)


while True:
    msg, client_addr = receive()
    
    if msg:
        handle_msg(msg, client_addr)

        
