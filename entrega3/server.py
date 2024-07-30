import socket as skt    #importando as bibliotecas
import random
from acomodacao import *

#Setando as informações do socket
ip = 'localhost' # IP do sevidor
server_port = 12000
server_socket = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)
server_addr = (ip, server_port)
server_socket.bind(server_addr) 
print('server is ready to receive')


users = {} # lista de clientes conectados
acmds = {} # lista de acomodações
list_seq = {} # lista com números de sequência para cada usuário

def make_pkt(seq_number, data):
    return str({'seq_number': seq_number, 'data': data}).encode()

def send(cmd, socket, addr):
    while True:
        socket.settimeout(3)
        seq = list_seq[addr]
        pkt = make_pkt(seq, cmd)

        if random.random() > 0.1:
            socket.sendto(pkt, addr)
            print('sending')
        try:
            msg, address = socket.recvfrom(1024)
            msg = eval(msg.decode())

            while msg is None:      
                msg, address = socket.recvfrom(1024)
                msg = eval(msg.decode())

            if msg['data'] == b'ACK' and msg['seq_number'] == seq:
                list_seq.update({addr: 1 - seq})
                print('ACK received')
                break
        except skt.timeout:
            # socket.sendto(pkt, addr)
            print('timeout')
            pass


def receive(socket):
    while True:
        socket.settimeout(3)
        
        try:
            seq = ""
            msg, address = socket.recvfrom(4096)
            msg = eval(msg.decode())

            if msg is None:
                continue

            if address not in list_seq:
                list_seq.update({address: 0})
          
            seq = list_seq.get(address)


            if msg['seq_number'] == seq and msg['data'] != b'ACK':
                print('msg received: ', msg['data'], 'and seq_number: ', msg['seq_number'])
                pkt = make_pkt(seq, b'ACK')
                socket.sendto(pkt, address)
                list_seq.update({address: 1 - seq})
                return msg['data'], address
            elif msg['seq_number'] != seq:
                print('quero seq ', seq, 'mas recebi ', msg['seq_number'])
                pkt = make_pkt(msg['seq_number'], b'ACK')
                socket.sendto(pkt, address)
                return "", address
                
        except skt.timeout:
            continue


def send_to_all(msg, socket):
    for user in users:
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
                response = f'você está online!'

        elif msg.startswith('list'):
            data = msg.split(':')[1]
            if(data == 'acmd'):
                response = 'Acomodações disponíveis:\n'
            else:
                response = 'Usuários online:\n'
                for user in users:
                    response += f'{user}\n'

        elif msg.startswith('create'):
            # create <nome_da_acomodação> <localização> <descricao>
            data = msg.split(' ')

            # checa se pode ser criada a acomodação
            for acmd in acmds:
                if acmd.nome == data[1] and acmd.localizacao == data[2]:
                    response = 'acomodação já existe'
                    send(response, server_socket, client_addr)
                    return
            
            # pega o nome do usuário
            user = [name for name, addr in users.items() if addr == client_addr][0]
            
            acmd = acomodacao(user, data[1], data[2], data[3])
            acmds[acmd.id] = acomodacao
            
            # informa a todos is usuários que uma nova acomodação foi criada
            ip, porta = client_addr
            alarm = '[{user}/{ip}:{porta}] nova acomodação: {acmd.nome} em {acmd.localizacao}'
            send_to_all(alarm, server_socket)

            response = 'acomodação de nome ' + data[1] + ' criada com sucesso!'
        else:
            response = 'comando inválido'
    
    send(response, server_socket, client_addr)


try:
    while True:
        msg, client_addr = receive(server_socket)
        
        if msg and msg != "":
           handle_msg(msg, client_addr)
except KeyboardInterrupt:
    server_socket.close()
        
