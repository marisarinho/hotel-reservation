## **Hotel Reservation Protocol (HRCP)**

### **Estrutura do Protocolo:**
Cada requisição enviada para o servidor deverá seguir a seguinte estrutura:<br>

**method:** O tipo de operação a ser realizada. Exemplos de métodos: CADASTRAR, LOGIN, RESERVAR, etc.<br>
**data:** Um objeto contendo os dados necessários para o método (como CPF, nome, número de quarto, etc.).<br>



### **Métodos e Descrições:**


**1. CADASTRAR**<br>
Descrição: Permite que o usuário se cadastre no sistema. A requisição deve conter o CPF, nome, telefone e senha do usuário.<br>

Exemplo de Requisição:<br>
{<br>
  "method": "CADASTRAR",<br>
  "data": {<br>
    "cpf": "12345678900",<br>
    "nome": "João",<br>
    "telefone": "987654321",<br>
    "senha": "senha123"<br>
  }<br>
}<br>
Status de Resposta:<br>

200: Hóspede cadastrado com sucesso.<br>
400: Já está cadastrado.<br>
401: Erro ao cadastrar.<br>


**2. LOGIN**<br>
Descrição: Permite que o hóspede se autentique no sistema. A requisição deve conter o CPF e a senha do usuário.<br>

Exemplo de Requisição:<br>
{<br>
  "method": "LOGIN",<br>
  "data": {<br>
    "cpf": "12345678900",<br>
    "senha": "senha123"<br>
  }<br>
}<br>
Status de Resposta:<br>

200: Hóspede logado com sucesso.<br>
401: CPF ou senha incorretos.<br>
402: Já está logado.<br>


**3. RESERVAR**<br>
Descrição: Permite que o hóspede faça uma reserva de quarto no hotel. A requisição deve conter o número do quarto, data de entrada e data de saída.<br>

Exemplo de Requisição:<br>

{<br>
  "method": "RESERVAR",<br>
  "data": {<br>
    "num_quarto": 101,<br>
    "data_entrada": "2025-03-20",<br>
    "data_saida": "2025-03-25"<br>
  }<br>
}<br>
Status de Resposta:<br>

201: Reserva confirmada.<br>
409: Quarto já reservado.<br>
401: É necessário fazer login.<br>


**4. CANCELAR**<br>
Descrição: Permite que o hóspede cancele uma reserva já feita. A requisição deve conter o número do quarto e a data de entrada.<br>

Exemplo de Requisição:<br>

{<br>
  "method": "CANCELAR",<br>
  "data": {<br>
    "num_quarto": 101,<br>
    "data_entrada": "2025-03-20"<br>
  }<br>
}<br>
Status de Resposta:<br>

200: Reserva cancelada com sucesso.<br>
400: Reserva não encontrada.<br>
401: É necessário fazer login.<br>


**5. CONSULTAR**<br>
Descrição: Permite que o hóspede consulte suas reservas feitas no hotel. A requisição deve conter o ano para filtrar as reservas.<br>

Exemplo de Requisição:<br>
{<br>
  "method": "CONSULTAR",<br>
  "data": {<br>
    "ano": 2025<br>
  }<br>
}<br>
Status de Resposta:<br>

200: Reservas encontradas.<br>
400: Não existem reservas para o ano solicitado.<br>
401: É necessário fazer login.<br>


**6. ADICIONAR**<br>
Descrição: Permite que o administrador adicione um novo quarto ao hotel. A requisição deve conter o número do quarto, preço e tipo de cama.<br>

Exemplo de Requisição:<br>

{<br>
  "method": "ADICIONAR",<br>
  "data": {<br>
    "num_quarto": 102,<br>
    "preco": 250.0,<br>
    "cama": "Queen"<br>
  }<br>
}<br>
Status de Resposta:<br>

200: Quarto adicionado com sucesso.<br>
400: Erro ao adicionar quarto.<br>

**7. LISTAR**<br>
Descrição: Permite que o administrador liste todos os quartos disponíveis no hotel.<br>

Exemplo de Requisição:<br>

{<br>
  "method": "LISTAR",<br>
  "data": {}<br>
}<br>
Status de Resposta:<br>

200: Lista de quartos disponíveis.<br>

**8. SAIR**<br>
Descrição: Permite que o cliente encerre a conexão com o servidor.<br>

Exemplo de Requisição:<br>

{<br>
  "method": "SAIR",<br>
  "data": {}<br>
}
Status de Resposta:
<br>
200: Conexão encerrada com sucesso.<br>
400: Erro ao encerrar a conexão.<br>
Erro de Requisição<br>
0: Bad Request - Formato incorreto de requisição.<br>

Exemplo de resposta do servidor:<br>

{<br>
  "codigo": 200,<br>
  "mensagem": "Reserva realizada com sucesso",<br>
  "dados": {<br>
    "num_quarto": 101,<br>
    "data_entrada": "2025-03-20",<br>
    "data_saida": "2025-03-25"<br>
  }<br>
}<br>