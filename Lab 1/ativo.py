# Lab 1 Ativo 
# Autor: Alex Pungartnik Handel DRE 114147792

import socket

HOST = 'localhost'
PORTA = 6001

#inicializa o socket
sock = socket.socket()
sock.connect((HOST, PORTA)) 

#espera input do usuario e manda
print("codigo para terminar conexão: 'closeConnection'")
while True:
	msg=input("Digite sua mensagem: ")
	sock.send(str.encode(msg))
	msgRecebida = sock.recv(2048)
	if str(msgRecebida, encoding='utf-8')=="closeConnection": 
		print("conexão fechada")
		break
	else:
		print("ECHO " + str(msgRecebida, encoding='utf-8'))

#fecha
sock.close() 
