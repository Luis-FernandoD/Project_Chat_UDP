import socket
import threading

def main():
    HOST = ''  # Endereço IP do Servidor (deve ser o IP do servidor ou deixar vazio para aceitar qualquer conexão)
    PORT = 5000  # Porta que o Servidor está
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dest = (HOST, PORT)
    print('\n...Digite "eu voltarei" para sair...\n')
    
    username = input('Usuário> ')

    print('\nConectado')

    thread1 = threading.Thread(target=recebermsg, args=(udp,))
    thread2 = threading.Thread(target=enviarmsg, args=(udp, username))

    thread1.start()

    print("\nDigite <Olá> para continuar")
    passw = ""
    while passw != 'Olá':
        passw = input("--> ")
        if passw != 'Olá':
            print("\nSeja educado e diga Olá\n")
    
    thread2.start()

def recebermsg(udp):
    while True:
        try:
            msg = udp.recv(1024).decode('utf-8')
            print(msg + '\n')
        except Exception as e:
            print(f"\nErro ao receber mensagem: {e}")
            udp.close()
            break

def enviarmsg(udp, username):
    while True:
        try:
            msg = input("\n")
            if msg != 'eu voltarei':
                udp.sendto(f'<{username}> {msg}'.encode('utf-8'), udp.getpeername())
            else:
                print("Desconectando...")
                udp.close()
                break
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            udp.close()
            break

if __name__ == '__main__':
    main()
