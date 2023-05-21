import threading
import socket

clientes = []
lock = threading.Lock()

def main():
    udp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = socket.gethostbyname(socket.gethostname()) # Endereco IP do Servidor
    PORT = 5000 # Porta que o Servidor esta
    orig = (HOST, PORT)
    try:
        udp.bind(orig)
        udp.listen()
    except:
        return print("Erro de conexão")

    while True:
        cliente, addr = udp.accept()
        print("Conexão recebida de", addr)
        clientes.append(cliente)

        thread = threading.Thread(target=gerencmsg, args=(cliente,))
        thread.start()

def gerencmsg(cliente):
    while True:
        try:
            msg = cliente.recv(1024)
            if not msg:
                excluircliente(cliente)
                break
            transmicao(msg, cliente)

        except:
            excluircliente(cliente)
            break

def transmicao(msg, cliente):
    with lock:
        for numcliente in clientes:
            if numcliente != cliente:
                try:
                    numcliente.send(msg)
                except:
                    excluircliente(numcliente)

def excluircliente(cliente):
    with lock:
        clientes.remove(cliente)

main()
