# Lab 4 servidor 
# Autor: Alex Pungartnik Handel DRE 114147792

import socket
import select
import sys
import threading
import random

HOST = ''
PORTA = 7004

#lista de I/O
entradas = [sys.stdin]
listaSockets=[]
#lock
lock = threading.Lock()

#INUTIL?
#função que inicia o servidor e returna um socket
def iniciaServidor():
	# cria o socket 
	mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Internet( IPv4 + TCP) 
	mySocket.bind((HOST, PORTA))
	mySocket.listen(5) 
	mySocket.setblocking(False)
	entradas.append(mySocket)

	return mySocket

#INUTIL?
#função que estabelece conexão com socket cliente e retorna o socket do cliente e seu endereco
def aceitaConexao(socket):
	# estabelece conexao com o proximo cliente
	clienteSocket, endereco = socket.accept()

	# registra a nova conexao
	lock.acquire()
	conexoes[clienteSocket] = endereco 
	estadoClientes[clienteSocket] = "start"
	parClientes[clienteSocket] = ""
	usernames[clienteSocket] = " "
	lock.release()


	return clienteSocket, endereco

def iniciaNodes(n):
	for i in range(n):
		print("tentando criar " + str(i))
		mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Internet( IPv4 + TCP) 
		mySocket.bind((HOST, PORTA+i))
		mySocket.listen(5) 
		mySocket.setblocking(True)
		entradas.append(mySocket)
		listaSockets.append(mySocket)

def nodeBehavior(nodeSocket):
	nodeIP=nodeSocket.getsockname()[0]
	nodePort=nodeSocket.getsockname()[1]
	print(nodeSocket.getsockname())
	nodeID = hash(nodeSocket.getsockname())
	while True:
		clienteSocket, endereco = nodeSocket.accept()
		print(clienteSocket.getsockname())
		pass

			
def main():
	#socket=iniciaServidor()
	iniciaNodes(16)
	for i in listaSockets:
		nodeThread = threading.Thread(target=nodeBehavior, args=[i])
		nodeThread.start()
	print("Pronto para receber conexoes...")
	while True:
		#espera por qualquer entrada de interesse
		leitura, escrita, excecao = select.select(entradas, [], [])
		#tratar todas as entradas prontas
		for pronto in leitura:
			if pronto in listaSockets:  #pedido novo de conexao
				#clienteSocket, endr = aceitaConexao(socket)
				print ('bah')
				#cliente = threading.Thread(target=processaRequisicoes, args=(clienteSocket,endr))
				#cliente.start()
			elif pronto == sys.stdin: #entrada padrao
				cmd = input()
				if cmd == 'fim': #solicitacao de finalizacao do servidor
					if not conexoes: #somente termina quando nao houver clientes ativos
						socket.close()
						sys.exit()
					else: print("ha conexoes ativas")
				elif cmd == "lista":
					print("usuarios: ")
					for name in usernames:
						print(usernames[name])

main()