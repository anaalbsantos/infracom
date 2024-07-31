# infracom

Repositório dedicado ao projeto da disciplina de Infraestrutura de Comunicações.
## equipe
- Ana Laura Albuquerque Santos
- Ana Paula Sá Barreto Paiva da Cunha
- David Oscar da Silva
- Ícaro Augusto Melo de Souza
- Luan Thiers de Oliveira Pires



## como rodar

Para isso, é importante saber que devemos rodar o código do cliente enquanto o código do servidor estiver rodando. Primeiro, abra a pasta de qual entrega deseja testar, sabendo que:

🌸 1ª entrega: Comunicação udp simples para enviar arquivo ao servidor e este alterar seu nome

🌸 2ª entrega: Mesma interação da primeira entrega, mas implementando o protocolo rdt 3.0

🌸 3ª entrega: Sistema de acomodações com o uso do rdt 3.0

### para o servidor

rodar o arquivo do servidor com 'python server.py'

### para o cliente

rodar o arquivo do cliente com 'python client.py'

### enviando arquivos

O código do cliente irá pedir o nome do arquivo, juntamente com sua extensão, que se quer enviar. Foi testado com 'fortnight.txt' e 'nenem.jpg' que também se encontram nas pastas de cada entrega. O servidor deve devolver o arquivo com nome alterado.
