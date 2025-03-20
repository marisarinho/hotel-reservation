

# Sistema de reserva do hotel Check-In Dreams
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

## Pré-Requisitos para Execução 
Python: Versão 3.11 <br>
Numpy: (pip install numpy)<br>


## Protocolo da Aplicação:
[Acesse aqui.](ttps://github.com/marisarinho/hotel-reservation/blob/main/hrcp.md)<br>

## Instruções para Execução
**Clone o repositório:**
git clone https://github.com/marisarinho/hotel-reservation.git <br>

**Entre no diretório do projeto:**
cd hotel-reservation<br>

**Instale o Numpy caso não esteja instalado:**
pip install numpy<br>

## Rode o servidor:
cd server<br>
python servidor.py<br>

## Em outro terminal, rode n clientes:
cd client<br>
python cliente.py

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
