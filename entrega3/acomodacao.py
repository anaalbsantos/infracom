import random

class acomodacao:
    def __init__(self, dono, nome, localizacao, identificador):
        self.id = identificador
        self.dono = dono # deve ser o nome do user
        self.nome = nome
        self.localizacao = localizacao
        self.dias_disponiveis = ['17/07/2024', "18/07/2024", "19/07/2024", "20/07/2024", "21/07/2024", "22/07/2024"]
        self.reservas = [] # deve associar o nome dos users com as datas reservadas
    

    def get_reservas_from(self, user):
        return [data for data in self.reservas if self.reservas[data] == user]
    
    def get_user_from(self, data):
        for reserva in self.reservas:
            if reserva[0] == data:
                return reserva[1]
        return None

    def book(self, user, data):
        if data in self.dias_disponiveis:
            self.dias_disponiveis.remove(data)
            self.reservas.append((data, user))
            return True
        else:
            return False
    
    def cancel(self, user, data):
        if (data, user) in self.reservas:
            self.dias_disponiveis.append(data)
            self.reservas.remove((data, user))
            return True
        else:
            return False