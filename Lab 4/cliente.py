# Lab 2 Cliente 
# Autor: Alex Pungartnik Handel DRE 114147792

import socket
import select
import sys

HOST = 'localhost'
PORTA = 6001

def main():
	#inicializa o socket
	sock = socket.socket()
	sock.connect((HOST, PORTA))
	while True:
		msg=input("digite o nome de usuario: ")
		sock.send(str.encode(msg))
		msg=sock.recv(2048)
		msgRecebida = str(msg, encoding='utf-8')
		print("msgRecebida")
	sock.close() 

main()