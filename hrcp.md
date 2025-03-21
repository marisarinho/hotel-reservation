## **Hotel Reservation Protocol (HRCP)**

### **Estrutura do Protocolo:**
Cada requisição enviada para o servidor deverá seguir a seguinte estrutura:<br>

**method:** O tipo de operação a ser realizada. Exemplos de métodos: CADASTRAR, LOGIN, RESERVAR, etc.<br>
**data:** Um objeto contendo os dados necessários para o método (como CPF, nome, número de quarto, etc.).<br>



### **Métodos e Descrições:**


**1. CADASTRAR**<br>
Descrição: Permite que o usuário se cadastre no sistema. A requisição deve conter o CPF, nome, telefone e senha do usuário.<br>

Exemplo de Requisição:<br>
<!-- {<br>
  "method": "CADASTRAR",<br>
  "data": {<br>
    "cpf": "12345678900",<br>
    "nome": "João",<br>
    "telefone": "987654321",<br>
    "senha": "senha123"<br>
  }<br>
}<br> -->
CADASTRAR|{cpf}|{nome}|{telefone}|{senha}
Status de Resposta:<br>

200: Hóspede cadastrado com sucesso.<br>
401: Já está logado.<br>
402: Cpf em uso. <br>
403: Telefone com formato inválido.<br>
405: Cpf inválido.<br>


**2. LOGIN**<br>
Descrição: Permite que o hóspede se autentique no sistema. A requisição deve conter o CPF e a senha do usuário.<br>

Exemplo de Requisição:<br>
<!-- {<br>
  "method": "LOGIN",<br>
  "data": {<br>
    "cpf": "12345678900",<br>
    "senha": "senha123"<br>
  }<br>
}<br> -->
LOGIN|{cpf}|{senha}
Status de Resposta:<br>

211: Hóspede logado com sucesso.<br>
411: Já está logado.<br>
412: CPF ou senha incorretos.<br>


**3. RESERVAR**<br>
Descrição: Permite que o hóspede faça uma reserva de quarto no hotel. A requisição deve conter o número do quarto, data de entrada e data de saída.<br>

Exemplo de Requisição:<br>

<!-- {<br>
  "method": "RESERVAR",<br>
  "data": {<br>
    "num_quarto": 101,<br>
    "data_entrada": "2025-03-20",<br>
    "data_saida": "2025-03-25"<br>
  }<br>
}<br> -->
RESERVAR|{num_quarto}|{data_entrada}|{data_saida}
Status de Resposta:<br>

221: Reserva confirmada.<br>
421: Precisa estar logado.<br>
422: Hospede não encontrado.<br>
423: Formato de data inválido.<br>
424: Quarto não cadastrado.<br>
425: O quarto já reservado <br>


**4. CANCELAR**<br>
Descrição: Permite que o hóspede cancele uma reserva já feita. A requisição deve conter o número do quarto e a data de entrada.<br>

Exemplo de Requisição:<br>

<!-- {<br>
  "method": "CANCELAR",<br>
  "data": {<br>
    "num_quarto": 101,<br>
    "data_entrada": "2025-03-20"<br>
  }<br>
}<br> -->
CANCELAR|{num_quarto}|{data_entrada}
Status de Resposta:<br>

231: Reserva cancelada com sucesso.<br>
431: É necessário fazer login.<br>
432: Reserva não encontrada.<br>


**5. CONSULTAR**<br>
Descrição: Permite que o hóspede consulte suas reservas feitas no hotel. A requisição deve conter o ano para filtrar as reservas.<br>

Exemplo de Requisição:<br>
<!-- {<br>
  "method": "CONSULTAR",<br>
  "data": {<br>
    "ano": 2025<br>
  }<br>
}<br> -->
CONSULTAR|{ano}
Status de Resposta:<br>

241: Reservas encontradas.<br>
441: É necessário fazer login.<br>
442: Reservas não encontradas.<br>
443: Hópede não encontrado. <br>


**6. ADICIONAR**<br>
Descrição: Permite que o administrador adicione um novo quarto ao hotel. A requisição deve conter o número do quarto, preço e tipo de cama.<br>

Exemplo de Requisição:<br>

<!-- {<br>
  "method": "ADICIONAR",<br>
  "data": {<br>
    "num_quarto": 102,<br>
    "preco": 250.0,<br>
    "cama": "Queen"<br>
  }<br>
}<br> -->
ADICIONAR|{num_quarto}|{preco}|{cama}
Status de Resposta:<br>

251: Quarto adicionado com sucesso.<br>
451: Quarto já existe.<br>
452: Formato inválido para quarto.<br>

**7. LISTAR**<br>
Descrição: Permite que o administrador liste todos os quartos disponíveis no hotel.<br>

Exemplo de Requisição:<br>

<!-- {<br>
  "method": "LISTAR",<br>
  "data": {}<br>
}<br> -->
LISTAR
Status de Resposta:<br>

261: Lista de quartos disponíveis.<br>

**8. SAIR**<br>
Descrição: Permite que o cliente encerre a conexão com o servidor.<br>

Exemplo de Requisição:<br>

<!-- {<br>
  "method": "SAIR",<br>
  "data": {}<br>
} -->
SAIR
Status de Resposta:
<br>
271: Conexão encerrada com sucesso.<br>
470: Erro ao encerrar a conexão.<br>
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