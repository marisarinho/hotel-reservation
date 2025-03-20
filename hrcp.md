##Hotel Reservation Protocol (HRCP)
Estrutura do Protocolo:
Cada requisição enviada para o servidor deverá seguir a seguinte estrutura:

method: O tipo de operação a ser realizada. Exemplos de métodos: CADASTRAR, LOGIN, RESERVAR, etc.
data: Um objeto contendo os dados necessários para o método (como CPF, nome, número de quarto, etc.).
Exemplo de requisição para RESERVAR:

json
Copiar código
{
  "method": "RESERVAR",
  "data": {
    "num_quarto": 101,
    "data_entrada": "2025-03-20",
    "data_saida": "2025-03-25"
  }
}
⚡ Métodos e Descrições:
1. CADASTRAR
📖 Descrição: Permite que o usuário se cadastre no sistema. A requisição deve conter o CPF, nome, telefone e senha do usuário.

Exemplo de Requisição:

json
Copiar código
{
  "method": "CADASTRAR",
  "data": {
    "cpf": "12345678900",
    "nome": "João",
    "telefone": "987654321",
    "senha": "senha123"
  }
}
Status de Resposta:

200: Hóspede cadastrado com sucesso.
400: Já está cadastrado.
401: Erro ao cadastrar.
2. LOGIN
📖 Descrição: Permite que o hóspede se autentique no sistema. A requisição deve conter o CPF e a senha do usuário.

Exemplo de Requisição:

json
Copiar código
{
  "method": "LOGIN",
  "data": {
    "cpf": "12345678900",
    "senha": "senha123"
  }
}
Status de Resposta:

200: Hóspede logado com sucesso.
401: CPF ou senha incorretos.
402: Já está logado.
3. RESERVAR
📖 Descrição: Permite que o hóspede faça uma reserva de quarto no hotel. A requisição deve conter o número do quarto, data de entrada e data de saída.

Exemplo de Requisição:

json
Copiar código
{
  "method": "RESERVAR",
  "data": {
    "num_quarto": 101,
    "data_entrada": "2025-03-20",
    "data_saida": "2025-03-25"
  }
}
Status de Resposta:

201: Reserva confirmada.
409: Quarto já reservado.
401: É necessário fazer login.
4. CANCELAR
📖 Descrição: Permite que o hóspede cancele uma reserva já feita. A requisição deve conter o número do quarto e a data de entrada.

Exemplo de Requisição:

json
Copiar código
{
  "method": "CANCELAR",
  "data": {
    "num_quarto": 101,
    "data_entrada": "2025-03-20"
  }
}
Status de Resposta:

200: Reserva cancelada com sucesso.
400: Reserva não encontrada.
401: É necessário fazer login.
5. CONSULTAR
📖 Descrição: Permite que o hóspede consulte suas reservas feitas no hotel. A requisição deve conter o ano para filtrar as reservas.

Exemplo de Requisição:

json
Copiar código
{
  "method": "CONSULTAR",
  "data": {
    "ano": 2025
  }
}
Status de Resposta:

200: Reservas encontradas.
400: Não existem reservas para o ano solicitado.
401: É necessário fazer login.
6. ADICIONAR
📖 Descrição: Permite que o administrador adicione um novo quarto ao hotel. A requisição deve conter o número do quarto, preço e tipo de cama.

Exemplo de Requisição:

json
Copiar código
{
  "method": "ADICIONAR",
  "data": {
    "num_quarto": 102,
    "preco": 250.0,
    "cama": "Queen"
  }
}
Status de Resposta:

200: Quarto adicionado com sucesso.
400: Erro ao adicionar quarto.
7. LISTAR
📖 Descrição: Permite que o administrador liste todos os quartos disponíveis no hotel.

Exemplo de Requisição:

json
Copiar código
{
  "method": "LISTAR",
  "data": {}
}
Status de Resposta:

200: Lista de quartos disponíveis.
8. SAIR
📖 Descrição: Permite que o cliente encerre a conexão com o servidor.

Exemplo de Requisição:

json
Copiar código
{
  "method": "SAIR",
  "data": {}
}
Status de Resposta:

200: Conexão encerrada com sucesso.
400: Erro ao encerrar a conexão.
⚠️ Erro de Requisição
0: Bad Request - Formato incorreto de requisição.
Exemplo de resposta do servidor:
json
Copiar código
{
  "codigo": 200,
  "mensagem": "Reserva realizada com sucesso",
  "dados": {
    "num_quarto": 101,
    "data_entrada": "2025-03-20",
    "data_saida": "2025-03-25"
  }
}