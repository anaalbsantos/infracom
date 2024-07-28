class acomodacao:
    def __init__(self, dono, nome, localizacao, descricao):
        self.id = id
        self.dono = dono # deve ser o nome do user
        self.nome = nome
        self.localizacao = localizacao
        self.descricao = descricao
        self.dias_disponiveis = ['17/07/2024', "18/07/2024", "19/07/2024", "20/07/2024", "21/07/2024", "22/07/2024"]
        self.reservas = [] # deve associar o nome dos users com as datas reservadas
    
    def get_reservas_from(self, user):
        return [data for data in self.reservas if self.reservas[data] == user]