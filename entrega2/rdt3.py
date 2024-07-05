def make_pkt(seq_number, data):
    return str({'seq_number': seq_number, 'data': data}).encode()

def udt_send(skt, pkt, addr):
    skt.sendto(pkt, addr)
    skt.settimeout(1)

    ack = False
    
    #n sei mt oq to fazendo
    while (not ack) & (not skt.TimeoutError):
        try:
            msg, addr = skt.recvfrom(1024)
        except skt.TimeoutError:
            skt.sendto(pkt, addr)
            skt.settimeout(1)

# def rdt_rcv(skt):
