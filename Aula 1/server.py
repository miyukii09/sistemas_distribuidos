import socket

# Criando socket TCP/IP
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(('localhost', 12345)) # IP e Porta 
servidor.listen(1)

print("Agardando conexão...")
conexao, endereco = servidor.accept()
print(f"Conectado por: {endereco}")

mensagem = conexao.recv(1024).decode()
print(f"Mensagem recebida: {mensagem}")

conexao.close()