import socket
import threading

# Função para lidar com cada cliente em uma thread separada
def lidar_com_cliente(conexao, endereco):
    try:
        # Recebe o nome do cliente
        nome_cliente = conexao.recv(1024).decode()
        if not nome_cliente:  # Cliente desconectou antes de enviar o nome
            nome_cliente = "Desconhecido"
        print(f"{nome_cliente} conectado em: {endereco} (Thread: {threading.current_thread().name})")

        mensagem = ""
        while mensagem != "sair":
            try:
                mensagem = conexao.recv(1024).decode()
                if not mensagem:  # Cliente desconectou
                    break
                print("")
                print(f"{nome_cliente}: {mensagem}")
                # Envia resposta ao cliente
                resposta = f"mensagem recebida: {mensagem}"
                conexao.send(resposta.encode())
            except Exception as e:
                print(f"Erro ou {nome_cliente} desconectado: {e}")
                break

        conexao.close()
        print(f"Conexão com {nome_cliente} ({endereco}) fechada")
    except Exception as e:
        print(f"Erro ao processar cliente em {endereco}: {e}")
        conexao.close()

# Criando socket TCP/IP
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Permite reutilizar a porta
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    servidor.bind(('0.0.0.0', 12345)) # Escuta em todas as interfaces
    servidor.listen(5)  # Permite mais conexões na fila
    print("Aguardando conexões...")
except Exception as e:
    print(f"Erro ao iniciar o servidor: {e}")
    servidor.close()
    exit(1)

while True:
    try:
        conexao, endereco = servidor.accept()
        # Cria uma thread para lidar com o cliente
        thread = threading.Thread(target=lidar_com_cliente, args=(conexao, endereco))
        thread.start()
    except KeyboardInterrupt:
        print("\nServidor encerrado pelo usuário")
        break
    except Exception as e:
        print(f"Erro ao aceitar conexão: {e}")
        break

servidor.close()
print("Servidor finalizado")