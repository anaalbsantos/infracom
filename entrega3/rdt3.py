import socket    #importando as bibliotecas
import random
from acomodacao import *

class connection:
    users = {}
    connected = True

    def open_socket(self, ip, port, type):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (ip, port)
        self.type = type
        print(type, 'on')
        if type == 'server':
            self.sock.bind(self.server_address)
        else:
            self.connect('server', self.server_address)  
    
    def connect(self, user, address):
        #print('address:', address)
        seq_number = 0 if not address in self.users.keys() else self.users[address]['seq_number']
        self.users[address] = {
            'user': user,
            'seq_number': seq_number
        }
        # print('user', user, 'connected')
    
    def make_pkt(self, seq_number, data):
        return str({'seq_number': seq_number, 'data': data}).encode()
    
    def update_seq_number(self, address = ''):
        #print('update seq -', address)
        if not address:
            address = self.server_address
        
        self.users[address]['seq_number'] = 1 - self.users[address]['seq_number']
        #print('new seq -', self.users[address]['seq_number'])
    
    def get_seq_number(self, address = ''):
        if not address:
            address = self.server_address
        
        if address in self.users:
            return self.users[address]['seq_number']
        else:
            self.connect(address[1], address)
            return self.users[address]['seq_number']
    
    def send(self, cmd, address = ''):
        ack = False
        if not address:
            address = self.server_address

        while not ack:
            self.sock.settimeout(3)
            pkt = self.make_pkt(self.get_seq_number(address), cmd)

            
            self.sock.sendto(pkt, address)
            # print('sending ', pkt, ' to ', address)

            msg, address = None, None

            try:
                msg, address = self.sock.recvfrom(4096)
            except socket.timeout:
                print('timeout')
            if msg is not None:
                msg = eval(msg.decode())

                if msg['data'] == b'ACK' and msg['seq_number'] == self.get_seq_number(address):
                    self.update_seq_number(address)
                    # print('ACK received')
                    ack = True
                

    def receive(self):
        while True:   
            msg, address = self.sock.recvfrom(4096)
            msg = eval(msg.decode())

            if msg['seq_number'] == self.get_seq_number(address) and msg['data'] != b'ACK':
                # print('msg received: ', msg['data'], 'and seq_number: ', msg['seq_number'])
                pkt = self.make_pkt(self.get_seq_number(address), b'ACK')
                self.sock.sendto(pkt, address)
                self.update_seq_number(address)
                return msg['data'], address
            elif msg['seq_number'] != self.get_seq_number(address):
                # print('quero seq ', self.get_seq_number(address), 'mas recebi ', msg['seq_number'])
                pkt = self.make_pkt(1 - self.get_seq_number(address), b'ACK')
                self.sock.sendto(pkt, address)
    
    def broadcast(self, msg, owner):
        for user in self.users:
            if self.users[user]['user'] != owner:
                # print( self.users[user]['user'], '-', user)
                self.send(msg, user)

    def print_users(self):
        print('----Users----')
        for user in self.users.values():
            print(user['user'])
        print('-------------')
    
    def get_users(self):
        usernames = []
        for user in self.users.values():
            usernames.append(user['user'])
        return usernames
    
    def get_user(self, address):
        if address in self.users:
            return self.users[address]['user']
        return None
    
    def has_message(self):
        return self.sock.recv is not None

    def disconnect(self, address):
        if address in self.users:
            print(str(self.users[address]['user']) + ' disconnected')
            del self.users[address]
    
    def remove_user(self, addr):
        if addr in self.users:
            del self.users[addr]
    
    def close_connection(self):
        self.connected = False
        self.sock.close()
        print('\nclosing socket')