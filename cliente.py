import socket
import threading

def main():
    HOST = ''  # Endereço IP do Servidor
    PORT = 5000  # Porta que o Servidor está
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP no lugar de TCP
    dest = ('localhost', PORT)  # Você deve usar o IP de destino do servidor, por exemplo, 'localhost' ou um IP real
    print('\n...Digite "eu voltarei" para sair...\n')
    passw = ""

    # Não há necessidade de usar connect() em UDP
    # udp.connect(dest)  # Remova isto!

    username = input('Usuário> ')
    print('\nConectado')

    # Inicia thread para receber mensagens
    thread1 = threading.Thread(target=recebermsg, args=(udp,))
    thread1.start()

    print("\nDigite <Olá> para continuar\n")
    while True:
        if passw != 'Olá':
            print("\nSeja educado e diga Olá\n")
            passw = input("--> ")
        else:
            thread2 = threading.Thread(target=enviarmsg, args=(udp, username, dest))
            thread2.start()
            break

# Função para receber mensagens
def recebermsg(udp):
    while True:
        try:
            msg, addr = udp.recvfrom(1024)  # Usando recvfrom() para UDP, que retorna o endereço de origem
            print(f"Mensagem recebida de {addr}: {msg.decode('utf-8')}\n")
        except Exception as e:
            print(f"\nErro ao receber a mensagem: {e}")
            udp.close()
            break

# Função para enviar mensagens
def enviarmsg(udp, username, dest):
    while True:
        try:
            msg = input("\n")
            if msg != 'eu voltarei':
                udp.sendto(f'<{username}> {msg}'.encode('utf-8'), dest)  # Usando sendto() para UDP
            else:
                udp.close()
                return
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return

# Chama a função principal para rodar o programa
main()
