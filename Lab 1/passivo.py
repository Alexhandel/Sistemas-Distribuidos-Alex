# Lab 1 passivo 
# Autor: Alex Pungartnik Handel DRE 114147792

import socket

HOST = ''
PORTA = 6001

#inicializa o socket e coloca em modo de espera
sock = socket.socket() 
sock.bind((HOST, PORTA))
sock.listen(1) 

#aceita conexão
novoSock, endereco = sock.accept()
print ('Conectado com: ', endereco)

#loop que recebe mensagem e manda de volta
while True:
	msg = novoSock.recv(1024)
	novoSock.send(msg)
	if str(msg, encoding='utf-8') == "closeConnection":
		print("fechando conexão")
		break

#fecha
novoSock.close() 
sock.close() 
