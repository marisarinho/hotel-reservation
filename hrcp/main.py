import socket
import curses

def menu(stdscr):
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect(("localhost", 12345))
    
    opcoes = ["Fazer Reserva", "Cancelar Reserva", "Listar Reservas", "Consultar Reserva", "Sair"]
    selecionado = 0
    
    curses.curs_set(0)  # Oculta o cursor
    stdscr.clear()
    
    while True:
        stdscr.clear()
        stdscr.addstr(0, 5, "Sistema de Reservas", curses.A_BOLD)
        
        for i, opcao in enumerate(opcoes):
            if i == selecionado:
                stdscr.addstr(i + 2, 5, opcao, curses.A_REVERSE)
            else:
                stdscr.addstr(i + 2, 5, opcao)
        
        tecla = stdscr.getch()
        
        if tecla == curses.KEY_UP and selecionado > 0:
            selecionado -= 1
        elif tecla == curses.KEY_DOWN and selecionado < len(opcoes) - 1:
            selecionado += 1
        elif tecla == ord('\n'):
            if selecionado == 0:  # Fazer Reserva
                stdscr.clear()
                stdscr.addstr(2, 5, "Digite seu CPF: ")
                stdscr.refresh()
                cpf = stdscr.getstr(3, 5, 20).decode()
                stdscr.addstr(4, 5, "Número do quarto: ")
                stdscr.refresh()
                num_quarto = stdscr.getstr(5, 5, 5).decode()
                stdscr.addstr(6, 5, "Período da reserva: ")
                stdscr.refresh()
                periodo = stdscr.getstr(7, 5, 20).decode()
                mensagem = f"RESERVAR {cpf} {num_quarto} {periodo}"
                cliente_socket.send(mensagem.encode())
                resposta = cliente_socket.recv(1024).decode()
                stdscr.addstr(9, 5, f"Resposta: {resposta}")
                stdscr.refresh()
                stdscr.getch()
            elif selecionado == 1:  # Cancelar Reserva
                stdscr.clear()
                stdscr.addstr(2, 5, "Digite seu CPF: ")
                stdscr.refresh()
                cpf = stdscr.getstr(3, 5, 20).decode()
                stdscr.addstr(4, 5, "Número do quarto para cancelar: ")
                stdscr.refresh()
                num_quarto = stdscr.getstr(5, 5, 5).decode()
                mensagem = f"CANCELAR {cpf} {num_quarto}"
                cliente_socket.send(mensagem.encode())
                resposta = cliente_socket.recv(1024).decode()
                stdscr.addstr(7, 5, f"Resposta: {resposta}")
                stdscr.refresh()
                stdscr.getch()
            elif selecionado == 2:  # Listar Reservas
                cliente_socket.send("LISTAR_RESERVAS".encode())
                resposta = cliente_socket.recv(1024).decode()
                stdscr.clear()
                stdscr.addstr(2, 5, "Reservas:")
                stdscr.addstr(3, 5, resposta)
                stdscr.refresh()
                stdscr.getch()
            elif selecionado == 3:  # Consultar por CPF
                stdscr.clear()
                stdscr.addstr(2, 5, "Digite seu CPF: ")
                stdscr.refresh()
                cpf = stdscr.getstr(3, 5, 20).decode()
                mensagem = f"CONSULTAR {cpf}"
                cliente_socket.send(mensagem.encode())
                resposta = cliente_socket.recv(1024).decode()
                stdscr.addstr(5, 5, f"Resposta: {resposta}")
                stdscr.refresh()
                stdscr.getch()
            elif selecionado == 4:  # Sair
                cliente_socket.close()
                break

if __name__ == "__main__":
    curses.wrapper(menu)
