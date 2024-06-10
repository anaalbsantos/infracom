import socket as skt    # Importando as bibliotecas
import os
import math

# Setando as informações do socket
buffer_size = 1024
server_name = 'localhost'
server_port = 12000
client_port = 12001
server_addr = (server_name, server_port)  # Definindo a tupla que contem o IP e a Porta do servidor
client_addr = (server_name, client_port)  # Definindo a tupla que contem o IP e a Porta do cliente

client_socket = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)  # Criando socket do cliente para UDP
client_socket.bind(client_addr)

def receive_file(package_number):
    # Definindo o recebimento dos pacotes

    # Como primeiro enviamos o nome do nosso arquivo, recebemos ele com recvfrom
    encoded_name, addr = client_socket.recvfrom(buffer_size)
    # Passando o valor em bytes para string novamente
    name, tipo = encoded_name.decode().split('.')  # Separamos o nome do arquivo e o seu tipo
    file_path = name + '_recebido.' + tipo

    # Definindo o recebimento dos pacotes
    with open(file_path, 'wb') as new_file:  # Enviando como parametro o caminho do arquivo em questao e definindo como escrita em arquivo binario

        # Usando try para caso ocorra timeout o arquivo e o socket sejam propriamente fechados
        try:
            for i in range(0, package_number):
                package_data, client_addr = client_socket.recvfrom(buffer_size)  # recebendo pacotes
                new_file.write(package_data)
                client_socket.settimeout(10)  # Definindo timeout para 2 segundos
        except TimeoutError:
            new_file.close()
            client_socket.close()
            print('Timeout Error')

# Definindo o envio dos pacotes 
file_path = input('Digite o nome do arquivo que deseja enviar: ')
client_socket.settimeout(10)  # Definindo timeout para 10 segundos

with open(file_path, 'rb') as file:  # Enviando como parametro o caminho do arquivo e definindo como leitura e arquivo binario

    file_path_list = file_path.split('\\')  # Como em Windows o path e separado por \\, usamos o split para obter cada uma das pastas
    file_name = file_path_list[-1]  # Pegamos o ultimo elemento da lista, que sera justamente o nome do nosso arquivo

    client_socket.sendto(file_name.encode(), server_addr)  # Enviando o nome ja codificado para bytes para o servidor especificado pelo endereco definido na tupla (IP,Port)
    # Para definir o numero de pacotes, vamos dividir o tamanho do arquivo escolhido pelo tamanho do buffer, ja definido como 1024
    package_number = math.ceil(os.path.getsize(file_path) / buffer_size)
    backup = file.read()

    # Enviando o numero de pacotes para o servidor especificado em serverAddr
    client_socket.sendto(str(package_number).encode(), server_addr)  # Passando para string para que possa ser devidamente codificado em bytes
    
    chunks = [backup[i:i+buffer_size] for i in range(0, len(backup), buffer_size)] # chunks é uma lista em que cada índice guarda 1024 bytes
    
    for i in range(0, package_number):
        file_data = chunks[i]  # Atualizando file_data com os próximos 1024 bytes
        if client_socket.sendto(file_data, server_addr):  # Analisa se o envio dos dados foi bem sucedido
            pass  # Nada precisa ser feito aqui, apenas enviamos os dados

    print('file sent to the server!')
    receive_file(package_number)
    client_socket.close()
