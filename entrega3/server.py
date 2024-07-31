import socket as skt    #importando as bibliotecas
import random
from acomodacao import *
from rdt3 import *

acmds = {} # dicionário de acomodações
    

def handle_msg(msg, address):
    response = 'comando inválido'
    if msg.startswith('login '):
        user = msg.split(' ')[1]
        if user in server.get_users():
            response = 'usuario ja usado'
            server.send(response, address)
            server.remove_user(address)
        else:
            server.connect(user, address)
            response = 'voce esta online!'
            server.send(response, address)

    if msg.startswith('create'):
        msg = msg.split(' ')

        owner = server.users[address]['user']
        acmd = acomodacao(owner, msg[1], msg[2], msg[3]) # dono, nome, localizacao, id
        acmds[acmd.id] = acmd
        
        response = 'acomodação de nome ' + msg[1] + ' criada com sucesso!'
        server.send(response, address)

        # alertar todos os usuários
        ip,porta = address
        alarm = '['+ str(owner) + '/' + str(ip) + ':' + str(porta) +'] criou uma nova acomodação: ' + msg[1]
        server.broadcast(alarm, owner)

    elif msg.startswith('list'):
        msg = msg.split(':')

        if msg[1] == 'myacmd':
            owner = server.users[address]['user']
            my_acmds = [acmd for acmd in acmds.values() if acmd.dono == owner]

            if my_acmds == []:
                response = 'você não possui acomodações'
            else:
                # informações da acomodação com: nome, localização, dia disponíveis
                response = '---- minhas acomodações ----\n'
                for x in my_acmds:
                    response += 'nome: ' + x.nome + '\nlocalização: ' + x.localizacao + '\ndias disponíveis: ' + str(x.dias_disponiveis) + '\n'
                    if x.reservas != []: response += 'reservas: ' + str(x.reservas) + '\n'
                response += '-----------------------------'
            
            server.send(response, address)

        elif msg[1] == 'acmd':
            response = '\n\n---- acomodações disponíveis ----\n'
            for x in acmds.values():
                response += 'nome: ' + x.nome + '\nlocalização: ' + x.localizacao + '\ndias disponíveis: ' + str(x.dias_disponiveis) + '\n'
                # if x.reservas != []: response += 'reservas: ' + str(x.reservas) + '\n'
                response += '-----------------------------'
            
            server.send(response, address)

        elif msg[1] == 'myrsv':
            client = server.users[address]['user']
            my_rsvs = [acmd for acmd in acmds.values() if client in acmd.reservas]

            if my_rsvs == []:
                response = 'você não possui reservas'
            else:
                response = '---- minhas reservas ----\n'
                for x in my_rsvs:
                    owner = x.dono
                    ip, porta = server.get_address(owner)
                    response += '['+ str(owner) + '/' + str(ip) + ':' + str(porta) +'] reserva em' + x.nome + ' para os dias: ' + str(x.get_reservas_from(client)) + '\n'
            
            server.send(response, address)

    elif msg.startswith('book'):
        msg = msg.split('')
        acmd_owner = msg[1]
        acmd_id = msg[2]
        acmd_date = msg[3]

        if acmd_owner == server.users[address]['user']:
            response = 'você não pode reservar a sua própria acomodação'
        else:
            if acmds.get(acmd_id).book(acmd_owner, acmd_date):
                response = 'reserva feita com sucesso!'
            else:
                response = 'não foi possível fazer a reserva'
        
        server.send(response, address)
    
    elif msg.startswith('cancel'):
        msg = msg.split('')
        acmd_owner = msg[1]
        acmd_id = msg[2]
        acmd_date = msg[3]

        # quem reservou a oferta
        client = acmds[acmd.id].get_user_from(acmd_date)

        # quem cancelou a reserva
        ip, porta = address

        # resposta para o cliente
        if acmds.get(acmd_id).cancel(acmd_owner, acmd_date):
            response = 'reserva cancelada com sucesso!'
        else:
            response = 'não foi possível cancelar a reserva'
        server.send(response, address)
        
        # resposta para o dono da acomodação
        alarm = '['+ str(client) + '/' + str(ip) + ':' + str(porta) +'] cancelou a reserva em ' + str(acmd_id) + ' para o dia ' + str(acmd_date)
        server.send(alarm, server.get_address(acmd_owner))

        ip, porta = server.get_address(acmd_owner)
        # resposta para todos os usuários
        alarm = '['+ str(acmd_owner) + '/' + str(ip) + ':' + str(porta) +'] novas disponibilidades para a acomodação ' + str(acmd_id) + ' para o dia ' + str(acmd_date)
        server.broadcast(alarm, acmd_owner)

    if server.get_user(address) == address[1]:
        server.remove_user(address)
        

try:
    server = connection()
    server.open_socket('localhost', 12000, 'server')

    while True:
        msg, address = None, None
        try:
            msg, address = server.receive()
        except:
            pass

        if msg is not None:
            print('msg: ', msg)

            if msg == b'logout':
                server.disconnect(address)
            else:
                handle_msg(msg.decode(), address)
            
            server.print_users()


except KeyboardInterrupt:
    server.close_connection()