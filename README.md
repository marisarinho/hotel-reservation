

# Sistema de reserva de hotel 
#### O projeto consiste no desenvolvimento de um sistema de reserva de hotel, utilizando um modelo cliente-servidor para gerenciar reservas de quartos de forma eficiente.


## Autoras
 Maria Clara Almeida | gomes.almeida@academico.ifpb.edu.br<br>
Mariana dos Santos Sarinho | sarinho.mariana@academico.ifpb.edu.br


## Disciplinas
 Estrutura de Dados | professor: Alex Sandro da Cunha Rêgo<br>
Protocolos de Interconexão de Redes de Computadores | professor: Leonidas Francisco de Lima Júnior


## Descrição do problema
O projeto visa desenvolver um sistema de reserva de hotel que será executado no terminal, permitindo que múltiplos usuários realizem reservas simultaneamente. O sistema tem como objetivo oferecer uma solução eficiente e acessível para a gestão de reservas, garantindo a organização e controle das acomodações disponíveis no hotel.

## Estrutura dos Arquivos do Projeto

hrcp/<br>
├── client/<br>
│   ├── cliente.py  <br>
│   └── listaQuarto.py<br>
├── hrcp/<br>
│   ├── cliente-server/<br>
│   │   ├── __init__.py<br>
├── server/<br>
│   ├── estruturas/<br>
│   │   ├── hashtable.py <br> 
│   │   └── listaOrd.py <br>
│   ├── exception.py  <br>
│   ├── gerar_quartos.py  <br>
│   ├── gerenciamento.py  <br>
│   ├── hospede.py  <br>
│   ├── quarto.py  <br>
│   ├── reserva.py  <br>
│   ├── servidor.py <br>
│   └── tratarCorrida.py<br> 
├── .gitignore<br>
├── hrcp.md<br>
└── README.md <br>

<table>
  <tr>
    <th>Arquivo</th>
    <th>Responsabilidade</th>
  </tr>
  <tr>
    <td><code>cliente.py</code></td>
    <td>Atua como cliente do sistema de reservas. Estabelece conexão com o servidor, envia requisições e processa respostas. Possui um menu interativo para cadastro, login, reserva, cancelamento e consulta de quartos.</td>
  </tr>
  <tr>
    <td><code>gerenciamento.py</code></td>
    <td>Gerencia as operações principais, como cadastro de hóspedes, gerenciamento de quartos e manipulação de reservas.</td>
  </tr>
  <tr>
    <td><code>servidor.py</code></td>
    <td>Implementa o servidor que gerencia conexões via sockets, processa operações no GerenciadorReservas e retorna códigos de status.</td>
  </tr>
  <tr>
    <td><code>hospede.py</code></td>
    <td>Define a classe <code>Hospede</code>, representando um hóspede do sistema. Valida CPF e protege atributos com encapsulamento.</td>
  </tr>
  <tr>
    <td><code>quarto.py</code></td>
    <td>Define a classe <code>Quarto</code>, armazenando número, preço e quantidade de camas. Permite comparações entre quartos pelo número.</td>
  </tr>
  <tr>
    <td><code>reserva.py</code></td>
    <td>Define a classe <code>Reserva</code>, armazenando informações sobre o quarto, datas de entrada/saída e hóspede associado.</td>
  </tr>
  <tr>
    <td><code>gerar_quarto.py</code></td>
    <td>Contém a função <code>gerar_quartos</code>, que cria e adiciona automaticamente quartos na HashTable.</td>
  </tr>
  <tr>
    <td><code>tratar_corrida.py</code></td>
    <td>Define um lock global para evitar condições de corrida em operações concorrentes.</td>
  </tr>
  <tr>
    <td><code>estruturas/hashTable.py</code></td>
    <td>Implementa uma tabela hash para armazenar e gerenciar hóspedes e quartos de forma eficiente.</td>
  </tr>
  <tr>
    <td><code>estruturas/listaOrd.py</code></td>
    <td>Implementa uma lista ordenada encadeada para armazenar reservas, mantendo-as organizadas por data de entrada.</td>
  </tr>
</table>


## Pré-Requisitos para Execução 
Python: Versão 3.11 <br>
Numpy: (pip install numpy)<br>


## Protocolo da Aplicação:
[Acesse aqui.](https://github.com/marisarinho/hotel-reservation/blob/main/hrcp.md)<br>

## Instruções para Execução
**Clone o repositório:**
git clone https://github.com/marisarinho/hotel-reservation.git <br>

**Entre no diretório do projeto:**
cd hotel-reservation<br>

**Instale o Numpy caso não esteja instalado:**
pip install numpy<br>

**Rode o servidor:**
cd server<br>
python servidor.py<br>

**Em outro terminal, rode n clientes:**
cd client<br>
python cliente.py<br>

## Desenvolvedoras responsaveis pelo projeto




<table>
    <td align="center">
      <a href="https://github.com/euclaraalmeida">
        <img src="https://github.com/euclaraalmeida.png" width="120" height="120" style="border-radius: 50%; border: 3px solid #4CAF50;"/>
      </a>
      <br>
      <strong><a href="https://github.com/euclaraalmeida" style="text-decoration: none; color: #4CAF50;">Clara Almeida</a></strong>
    </td>
    <td align="center">
      <a href="https://github.com/marisarinho">
        <img src="https://github.com/marisarinho.png" width="120" height="120" style="border-radius: 50%; border: 3px solid #4CAF50;"/>
      </a>
      <br>
      <strong><a href="https://github.com/marisarinho" style="text-decoration: none; color: #4CAF50;">Mariana Sarinho</a></strong>
    </td>
  </tr>
</table>
