# Lab 4 Cliente 
# Autor: Alex Pungartnik Handel DRE 114147792

import socket
import threading

HOST = 'localhost'
PORTA = 7004

def recebeMensagem(mySocket):
	while True:
		data = mySocket.recv(2048)
		msg = data.decode("utf-8")
		print(msg)
		
def enviaMensagem(mySocket):
	while True:
		msg=input()
		mySocket.send(str.encode(msg))

def main():
	#inicializa o socket
	mySocket = socket.socket()
	mySocket.connect((HOST, PORTA))
	msg=input("digite o nome de usuario: ")
	mySocket.send(str.encode(msg))
	msg=mySocket.recv(2048)
	msgRecebida = str(msg, encoding='utf-8')
	print(msgRecebida)
	#cria uma thread pra mandar e uma pra receber
	sendThread = threading.Thread(target=enviaMensagem, args=[mySocket])
	receiveThread = threading.Thread(target=recebeMensagem, args=[mySocket])
	sendThread.start()
	receiveThread.start()
	while True:
		pass

main()