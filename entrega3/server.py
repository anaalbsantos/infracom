import socket as skt
import random
import threading
from acomodacao import *

# Setando as informações do socket
ip = 'localhost' # IP do servidor
server_port = 12000
server_socket = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)
server_addr = (ip, server_port)
server_socket.bind(server_addr)
print('server is ready to receive')

users = {}  # lista de clientes conectados
acmds = {}  # lista de acomodações

seq_number = 0
seq_lock = threading.Lock()

def make_pkt(seq_number, data):
    return str({'seq_number': seq_number, 'data': data}).encode()

def send(cmd, socket, addr):
    global seq_number
    attempts = 0
    while attempts < 5:  # Tentativas limitadas para evitar looping infinito
        pkt = make_pkt(seq_number, cmd)

        if random.random() > 0.1:
            socket.sendto(pkt, addr)
            print('sending')
        try:
            socket.settimeout(5)
            msg, address = socket.recvfrom(1024)
            msg = eval(msg.decode())

            if msg and msg['data'] == b'ACK' and msg['seq_number'] == seq_number:
                with seq_lock:
                    seq_number = 1 - seq_number
                print('ACK received')
                break
        except skt.timeout:
            print('resending')
            attempts += 1
            continue

def receive(socket):
    global seq_number
    while True:
        try:
            socket.settimeout(5)
            msg, address = socket.recvfrom(4096)
            msg = eval(msg.decode())
            if msg and msg['seq_number'] == seq_number and msg['data'] != b'ACK':
                print('msg received: ', msg['data'], 'and seq_number: ', msg['seq_number'])
                pkt = make_pkt(seq_number, b'ACK')
                socket.sendto(pkt, address)
                with seq_lock:
                    seq_number = 1 - seq_number
                return msg['data'], address
        except skt.timeout:
            continue

def send_to_all(msg, socket, exclude_addr=None):
    for user in users:
        if users[user] != exclude_addr:
            send(msg, socket, users[user])

def handle_msg(msg, client_addr):
    global users

    if client_addr not in users.values() and not msg.startswith('login'):
        response = 'você precisa logar primeiro'
    else:
        if msg.startswith('login'):
            if client_addr in users.values():
                response = 'você já está logado'
            else:
                name = msg.split(' ')[1]
                users[name] = client_addr
                print(f'{name} connected')
                response = 'você está online!'

        elif msg.startswith('list'):
            data = msg.split(':')[1]
            if data == 'acmd':
                response = 'Acomodações disponíveis:\n'
                for acmd in acmds.values():
                    response += f'{acmd.nome} em {acmd.localizacao}\n'
            else:
                response = 'Usuários online:\n'
                for user in users:
                    response += f'{user}\n'

        elif msg.startswith('create'):
            data = msg.split(' ')
            nome_acmd = data[1]
            localizacao_acmd = data[2]
            descricao_acmd = data[3]

            for acmd in acmds.values():
                if acmd.nome == nome_acmd and acmd.localizacao == localizacao_acmd:
                    response = 'acomodação já existe'
                    send(response, server_socket, client_addr)
                    return

            user = [name for name, addr in users.items() if addr == client_addr][0]

            new_acmd = acomodacao(user, nome_acmd, localizacao_acmd, descricao_acmd)
            acmds[new_acmd.id]=new_acmd 

            ip, porta = client_addr
            alarm = f'[{user}/{ip}:{porta}] nova acomodação: {new_acmd.nome} em {new_acmd.localizacao}'
            send_to_all(alarm, server_socket, exclude_addr=client_addr)

            response = f'acomodação de nome {nome_acmd} criada com sucesso!'
        else:
            response = 'comando inválido'

    send(response, server_socket, client_addr)

def client_handler(socket):
    while True:
        msg, client_addr = receive(socket)
        if msg:
            handle_msg(msg, client_addr)

try:
    for _ in range(5):
        threading.Thread(target=client_handler, args=(server_socket,)).start()
except KeyboardInterrupt:
    server_socket.close()
