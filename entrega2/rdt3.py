import random
import socket
def make_pkt(seq_number, data):
    return str({'seq_number': seq_number, 'data': data}).encode()

def udt_send(skt, seq, data, addr):
    pkt = make_pkt(seq, data)
    seq = 1 - seq
    
    skt.settimeout(1)

    ack = False
    
    while (not ack): # enquanto não receber o ACK correto, reenvia o pacote
        if(errorRandom()):
            skt.sendto(pkt, addr)

        try:
            msg, addr = skt.recvfrom(1024)
        except socket.timeout:
            print('Timeout! Resending packet...')
            # skt.sendto(pkt, addr)
            skt.settimeout(1)
        else:
            ack = define_ack(pkt, msg)
    
    skt.settimeout(None)

    return seq

def define_ack(pkt, msg):
    str_msg = eval(msg.decode())
    str_pkt = eval(pkt.decode())

    # print(str_msg['seq_number'], str_pkt['seq_number'])

    if str_msg['seq_number'] != str_pkt['seq_number']: # se o número de seq não for o esperado, não recebeu ACK correto
        return False
    
    return True

def rdt_rcv(skt, seq):
    pkt, addr = skt.recvfrom(4096)
    str_pkt = eval(pkt.decode())

    # print('Received packet!')

    if str_pkt['seq_number'] != seq:
        pkt = make_pkt(1 - seq, b'ACK')
        skt.sendto(pkt, addr)
    else:
        pkt = make_pkt(seq, b'ACK')
        skt.sendto(pkt, addr)
        seq = 1 - seq
    
    return str_pkt['data'], seq

def errorRandom():
    error = random.random()
    if(error <= 0.3):
        return False
    return True
    