import socket as skt    #importando as bibliotecas
import os
from time import sleep
import math
from rdt3 import *

#Setando as informações do socket
ip = 'localhost' # IP do sevidor
server_port = 12000
client_port = 12001
server_socket = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)
server_addr = (ip, server_port)
client_addr = (ip, client_port)
server_socket.bind(server_addr) # Configurando o socket do servidor
buffer_size = 1024 # Tamanho maximo do buffer
print('The server is ready to receive')

# Numero de sequencia para rdt3.0
seq_number = 0

# Definindo o retorno dos pacotes
def send_file(file_path1):
    global seq_number

    file_encoded = file_path1.encode() # passando o arquivo para bytes
    print('Sending file name to the client...')
    seq_number = udt_send(server_socket, seq_number, file_encoded, client_addr) # Enviando o nome do arquivo para o cliente
    print('Done!')
    
    
    with open(file_path1, 'rb') as file :
        print('Sending file to the client...')
        for i in range (0, package_number):
            file_data = file.read(buffer_size)
            seq_number = udt_send(server_socket, seq_number, file_data, client_addr)
            print(f"Package {i+1}/{package_number} sent")
    print('File sent to the client!')

try:
    while 1:

        # Como primeiro enviamos o path do nosso arquivo, recebemos ele
        encoded_name, seq_number = rdt_rcv(server_socket, seq_number)
        print('Received file name from the client!')

        # Passando o valor em bytes para string novamente
        name, tipo = (encoded_name.decode().split('\\')[-1]).split('.') # Separamos o nome do arquivo e o seu tipo
        file_path = name + '.' + tipo

        #Recebendo o numero de pacotes 
        data, seq_number = rdt_rcv(server_socket, seq_number)
        package_number = int(data.decode())

        # Recebendo o arquivo
        with open(file_path, 'wb') as new_file:
            try:
                server_socket.settimeout(10)  # Definindo timeout para 10 segundos
                for i in range(package_number):
                    # package_data, client_addr = server_socket.recvfrom(buffer_size)  # Recebendo pacotes
                    package_data, seq_number = rdt_rcv(server_socket, seq_number)
                    new_file.write(package_data)
                    print(f"Package {i+1}/{package_number} received")
                server_socket.settimeout(None)  # Desativando o timeout após a recepção
            except TimeoutError:
                print('Timeout Error: File reception incomplete')
        
        print(f'File received and saved as {file_path}')
        send_file(file_path)

except KeyboardInterrupt:
    server_socket.close()
    print('Server closed')