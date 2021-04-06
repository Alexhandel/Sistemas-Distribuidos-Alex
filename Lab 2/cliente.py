# Lab 2 Cliente 
# Autor: Alex Pungartnik Handel DRE 114147792

import socket

HOST = 'localhost'
PORTA = 6001

#inicializa o socket
sock = socket.socket()
sock.connect((HOST, PORTA)) 

#espera input do usuario e manda
#camada de interface
while True:
	msg=input("digite o nome do arquivo a ser analisado:")
	sock.send(str.encode(msg))
	msg=sock.recv(2048)
	msgRecebida = str(msg, encoding='utf-8')
	#condição checa se o arquivo foi recebido
	if msgRecebida=="fileFound":
		#recebe uma lista de palavras e uma de frequancias, já ordenadas
		palavra=sock.recv(2048)
		frequencia=sock.recv(2048)
		#converte os bytes pra string
		palavra=palavra.decode('utf-8')
		frequencia=frequencia.decode('utf-8')
		#converte as strings em lista
		palavra=eval(palavra)
		frequencia=eval(frequencia)
		#printa
		for i in range(0,10):
			print(str(palavra[i]) + " : " + str(frequencia[i]))
	else:
		print("arquivo não encontrado")

#fecha
sock.close() 

