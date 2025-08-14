import socket
import threading

# Contador para identificar clientes
contador_clientes = 0
lock = threading.Lock()  # Para evitar condições de corrida ao incrementar o contador

# Função para lidar com cada cliente em uma thread separada
def lidar_com_cliente(conexao, endereco, cliente_id):
    nome_cliente = f"Cliente {cliente_id}"
    print(f"{nome_cliente} conectado em: {endereco}")

    mensagem = ""
    while mensagem != "sair":
        try:
            mensagem = conexao.recv(1024).decode()
            if not mensagem:  # Cliente desconectou
                break
            print(f"Mensagem recebida do {nome_cliente}: {mensagem}")
            # Envia resposta ao cliente
            resposta = f"ola! recebi: {mensagem}"
            conexao.send(resposta.encode())
        except:
            print(f"Erro ou {nome_cliente} {endereco} desconectado")
            break

    conexao.close()
    print(f"Conexão com {nome_cliente} {endereco} fechada")

# Criando socket TCP/IP
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(('localhost', 12345)) # IP e Porta 
servidor.listen(5) # Aumentado para permitir mais conexões na fila

print("Agardando conexão...")
while True:
    try:
        conexao, endereco = servidor.accept()
        # Incrementa o contador de clientes com segurança
        with lock:
            contador_clientes += 1
            cliente_id = contador_clientes
        # Cria uma thread para lidar com o cliente
        thread = threading.Thread(target=lidar_com_cliente, args=(conexao, endereco, cliente_id))
        thread.start()
    except KeyboardInterrupt:
        print("\nServidor encerrado pelo usuário")
        break
    except:
        print("Erro ao aceitar conexão")
        break

servidor.close()