import threading
import socket

clientes = []
lock = threading.Lock()

def main():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Usando localhost ou um IP específico. Modifique conforme necessário.
    HOST = 'localhost'  # Ou você pode usar socket.gethostbyname(socket.gethostname())
    PORT = 5000  # Porta do servidor
    orig = (HOST, PORT)
    
    try:
        udp.bind(orig)
        print(f"Servidor UDP ouvindo na porta {PORT}...")
    except Exception as e:
        print(f"Erro de conexão: {e}")
        return
    
    while True:
        try:
            msg, addr = udp.recvfrom(1024)  # Recebe mensagem de qualquer cliente
            print(f"Mensagem recebida de {addr}: {msg.decode()}")
            
            # Adiciona o cliente à lista, se ainda não estiver
            if addr not in clientes:
                clientes.append(addr)

            # Criar thread para gerenciar a transmissão de mensagens
            thread = threading.Thread(target=transmicao, args=(msg, addr, udp))
            thread.daemon = True
            thread.start()

        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")
            break

def transmicao(msg, addr, udp):
    with lock:
        # Envia a mensagem para todos os clientes conectados, exceto o cliente que enviou
        for cliente in clientes:
            if cliente != addr:  # Não envia para o próprio cliente
                try:
                    udp.sendto(msg, cliente)
                except Exception as e:
                    print(f"Erro ao enviar para {cliente}: {e}")
                    excluircliente(cliente)

def excluircliente(cliente):
    with lock:
        try:
            clientes.remove(cliente)
            print(f"Cliente {cliente} desconectado.")
        except ValueError:
            pass  # Se o cliente não estiver na lista, ignora o erro

if __name__ == "__main__":
    main()
