import socket

# Ip do Servidor
Servidor = "localhost"

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((Servidor, 12345)) # IP e Porta 

# Pede ao usuário para digitar seu nome antes de conectar
nome = input("Digite seu nome: ")
if not nome:  # Garante que o nome não seja vazio
    nome = "Desconhecido"

try:

    # Envia o nome ao servidor
    cliente.send(nome.encode())

    mensagem = ""
    while mensagem != "sair":
        mensagem = input("Digite uma mensagem: ").strip()
        if not mensagem:  # Ignora mensagens vazias
            continue
        cliente.send(mensagem.encode())
        try:
            resposta = cliente.recv(1024).decode()
            if not resposta:  # Servidor desconectou
                print("Servidor desconectado")
                break
            print(f"Servidor: {resposta}")
        except Exception as e:
            print(f"Erro ou servidor desconectado: {e}")
            break

except Exception as e:
    print(f"Erro ao conectar ao servidor: {e}")

cliente.close()