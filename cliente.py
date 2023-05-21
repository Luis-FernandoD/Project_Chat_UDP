import socket
import threading

def main():
    HOST = ''  # Endereco IP do Servidor
    PORT = 5000  # Porta que o Servidor esta
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dest = (HOST, PORT)
    print('\n...Digite "eu voltarei" para sair...\n')
    passw = ""

    try:
        udp.connect(dest)
    except:
        return print("Não foi possível estabelecer uma conexão")

    username = input('Usuário> ')

    print('\nConectado')

    thread1 = threading.Thread(target=recebermsg, args=(udp,))
    thread2 = threading.Thread(target=enviarmsg, args=(udp, username))

    thread1.start()

    print("\nDigite <Olá> para continuar\n")
    while True:
        if passw != 'Olá':
            print("\nSeja educado e diga Olá\n")
            passw = input("--> ")
        else:
            thread2.start()
            break


def recebermsg(udp):
    while True:
        try:
            msg = udp.recv(1024).decode('utf-8')
            print(msg + '\n')
        except:
            print("\nHasta la vista")
            udp.close()
            break


def enviarmsg(udp, username):
    while True:
        try:
            msg = input("\n")
            if msg != 'eu voltarei':
                udp.send(f'<{username}> {msg}'.encode('utf-8'))
            else:
                udp.close()
                return
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return


main()
