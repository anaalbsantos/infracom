import socket as skt    # Importando as bibliotecas
import os
import math
from rdt3 import *

# Setando as informações do socket
buffer_size = 1024
server_name = 'localhost'
server_port = 12000
client_port = 12001
server_addr = (server_name, server_port)  # Definindo a tupla que contem o IP e a Porta do servidor
client_addr = (server_name, client_port)  # Definindo a tupla que contem o IP e a Porta do cliente

client_socket = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)  # Criando socket do cliente para UDP
client_socket.bind(client_addr)

#Numero de sequencia para rdt3.0
seq_number = 0

# Definindo o recebimento dos pacotes
def receive_file(package_number):
    global seq_number
    
    # Recebe nome do arquivo
    encoded_name, seq_number = rdt_rcv(client_socket, seq_number)
    print('Received file name from the server!')

    # Passando o valor em bytes para string novamente
    name, tipo = encoded_name.decode().split('.')  # Separamos o nome do arquivo do seu tipo
    file_path = name + '_recebido.' + tipo

    # Definindo o recebimento dos pacotes
    with open(file_path, 'wb') as new_file:

        # Usando try para caso ocorra timeout o arquivo e o socket sejam propriamente fechados
        try:
            for i in range(0, package_number):
                package_data, seq_number = rdt_rcv(client_socket, seq_number)
                new_file.write(package_data)
                client_socket.settimeout(10)
        except TimeoutError:
            new_file.close()
            client_socket.close()
            print('Timeout Error')
    print('File received from the server!')

# Definindo o envio dos pacotes 
file_path = input('Digite o nome do arquivo que deseja enviar: ')
client_socket.settimeout(10)

with open(file_path, 'rb') as file:

    file_path_list = file_path.split('\\')  # Como em Windows o path e separado por \\, usamos o split para obter cada uma das pastas
    file_name  = file_path_list[-1] # Pegamos o ultimo elemento da lista (nome do arquivo)

    # Enviando o nome do arquivo codificado em bytes para o servidor
    print('Sending file name to the server...')
    seq_number = udt_send(client_socket, seq_number, file_name.encode(), server_addr)
    print('Done!')
    
    # Definindo numero de pacotes
    package_number = math.ceil(os.path.getsize(file_path) / buffer_size)
    backup = file.read()
    
    # Enviando numero de pacotes para o servidor
    print('Sending number of packages to the server...')
    seq_number = udt_send(client_socket, seq_number, str(package_number).encode(), server_addr)
    print('Done!')
    
    # Lista com os pacotes a serem enviados
    chunks = [backup[i:i+buffer_size] for i in range(0, len(backup), buffer_size)]
    
    print('Sending file to the server...')
    for i in range(0, package_number):
        seq_number = udt_send(client_socket, seq_number, chunks[i], server_addr)    
        

    print('File sent to the server!')
    receive_file(package_number)
    client_socket.close()