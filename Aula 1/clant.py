import socket

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(("localhost", 12345)) # IP e Porta 

mensagem = input("Digita uma mensagem para o servidor: ")
cliente.send(mensagem.encode())

cliente.close()